from __future__ import annotations

import json
import math
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
ASSETS = ["SHY", "IEF", "TLT", "LQD", "HYG"]
BENCHMARK = "AGG"
START = "2010-01-01"
END = "2026-09-01"  # excludes the incomplete September 2026 month
TRAIN_END = "2018-12-31"
CAP = 0.45
ANNUALIZATION = 12

# Transparent scenario inputs, not historical or issuer-reported time series.
# Rate duration is a parallel-rate sensitivity proxy; spread duration applies
# only to credit sleeves. Key-rate weights sum to each sleeve's rate duration.
SCENARIO_INPUTS = {
    "SHY": {"rate_duration": 1.9, "spread_duration": 0.0, "krd_2y": 1.6, "krd_5y": 0.3, "krd_10y": 0.0, "krd_30y": 0.0},
    "IEF": {"rate_duration": 7.3, "spread_duration": 0.0, "krd_2y": 0.3, "krd_5y": 2.5, "krd_10y": 4.5, "krd_30y": 0.0},
    "TLT": {"rate_duration": 15.8, "spread_duration": 0.0, "krd_2y": 0.0, "krd_5y": 0.2, "krd_10y": 4.1, "krd_30y": 11.5},
    "LQD": {"rate_duration": 7.9, "spread_duration": 7.6, "krd_2y": 0.2, "krd_5y": 2.5, "krd_10y": 4.4, "krd_30y": 0.8},
    "HYG": {"rate_duration": 3.1, "spread_duration": 3.0, "krd_2y": 0.4, "krd_5y": 1.8, "krd_10y": 0.9, "krd_30y": 0.0},
}


def yahoo_chart(symbol: str, interval: str = "1mo") -> pd.DataFrame:
    p1 = int(pd.Timestamp(START, tz="UTC").timestamp())
    p2 = int(pd.Timestamp(END, tz="UTC").timestamp())
    params = urllib.parse.urlencode({"period1": p1, "period2": p2, "interval": interval, "events": "div,splits"})
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?{params}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.load(response)["chart"]["result"][0]
    q = result["indicators"]["quote"][0]
    adj = result["indicators"].get("adjclose", [{}])[0].get("adjclose", q["close"])
    out = pd.DataFrame({
        "date": pd.to_datetime(result["timestamp"], unit="s", utc=True).tz_localize(None),
        "adj_close": adj,
        "close": q["close"],
        "volume": q["volume"],
    }).dropna(subset=["adj_close", "close"])
    if interval == "1mo":
        out["period"] = out["date"].dt.to_period("M").dt.to_timestamp("M")
    else:
        out["period"] = out["date"].dt.normalize()
    return out.drop_duplicates("period", keep="last").set_index("period")


def fred_series(series: str) -> pd.Series:
    params = urllib.parse.urlencode({"id": series, "cosd": START, "coed": END, "fq": "Monthly", "fam": "Average"})
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?{params}"
    frame = pd.read_csv(url)
    frame.columns = ["date", series]
    frame["date"] = pd.to_datetime(frame["date"])
    frame[series] = pd.to_numeric(frame[series], errors="coerce")
    return frame.dropna().set_index("date")[series]


def annual_metrics(returns: pd.Series, benchmark: pd.Series | None = None) -> dict[str, float]:
    returns = returns.dropna()
    wealth = (1 + returns).cumprod()
    years = len(returns) / ANNUALIZATION
    cagr = wealth.iloc[-1] ** (1 / years) - 1
    vol = returns.std(ddof=1) * math.sqrt(ANNUALIZATION)
    drawdown = (wealth / wealth.cummax() - 1).min()
    result = {"cagr": cagr, "volatility": vol, "sharpe_0rf": cagr / vol if vol else np.nan, "max_drawdown": drawdown}
    if benchmark is not None:
        aligned = pd.concat([returns.rename("p"), benchmark.rename("b")], axis=1).dropna()
        active = aligned.p - aligned.b
        te = active.std(ddof=1) * math.sqrt(ANNUALIZATION)
        ann_active = active.mean() * ANNUALIZATION
        result.update({"active_return_arithmetic": ann_active, "tracking_error": te, "information_ratio": ann_active / te if te else np.nan})
    return result


def optimize_weights(train: pd.DataFrame, objective: str) -> np.ndarray:
    mean = train.mean().to_numpy() * ANNUALIZATION
    cov = train.cov().to_numpy() * ANNUALIZATION
    n = len(mean)
    def vol(w: np.ndarray) -> float:
        return float(np.sqrt(w @ cov @ w))
    def neg_sharpe(w: np.ndarray) -> float:
        return -float((w @ mean) / vol(w))
    fun = vol if objective == "min_vol" else neg_sharpe
    res = minimize(fun, np.repeat(1 / n, n), method="SLSQP", bounds=[(0, CAP)] * n, constraints={"type": "eq", "fun": lambda w: w.sum() - 1})
    if not res.success:
        raise RuntimeError(res.message)
    return res.x


def turnover_cost_returns(returns: pd.DataFrame, weights: np.ndarray, bps: float) -> pd.Series:
    # Monthly constant-mix rebalancing. Turnover is the one-way weight traded
    # after asset returns move the portfolio away from target weights.
    gross = returns @ weights
    drift = returns.add(1).mul(weights, axis=1)
    drift = drift.div(drift.sum(axis=1), axis=0)
    one_way_turnover = drift.sub(weights, axis=1).abs().sum(axis=1) / 2
    return gross - one_way_turnover * bps / 10_000


def run() -> None:
    DATA.mkdir(exist_ok=True)
    OUTPUTS.mkdir(exist_ok=True)
    raw = {}
    for symbol in ASSETS + [BENCHMARK]:
        frame = yahoo_chart(symbol)
        frame.to_csv(DATA / f"{symbol.lower()}_monthly.csv", index_label="month")
        raw[symbol] = frame

    prices = pd.concat({s: f.adj_close for s, f in raw.items()}, axis=1).dropna()
    returns = prices.pct_change().dropna()
    train = returns.loc[:TRAIN_END, ASSETS]
    test = returns.loc[pd.Timestamp(TRAIN_END) + pd.offsets.MonthEnd(1):, ASSETS]
    bench_test = returns.loc[test.index, BENCHMARK]

    weights = {
        "equal_weight": np.repeat(1 / len(ASSETS), len(ASSETS)),
        "minimum_volatility": optimize_weights(train, "min_vol"),
        "maximum_sharpe": optimize_weights(train, "max_sharpe"),
    }
    pd.DataFrame(weights, index=ASSETS).T.to_csv(OUTPUTS / "portfolio_weights.csv", index_label="portfolio")

    rows = []
    net_returns = {}
    for name, w in weights.items():
        for bps in [0, 5, 10]:
            r = turnover_cost_returns(test, w, bps)
            if bps == 10:
                net_returns[name] = r
            rows.append({"portfolio": name, "one_way_cost_bps": bps, **annual_metrics(r, bench_test)})
    metrics = pd.DataFrame(rows)
    metrics.to_csv(OUTPUTS / "out_of_sample_metrics.csv", index=False)
    net = pd.DataFrame(net_returns)
    net[BENCHMARK] = bench_test
    net.to_csv(OUTPUTS / "out_of_sample_monthly_returns.csv", index_label="month")
    (1 + net).cumprod().plot(figsize=(9, 5), linewidth=1.6)
    plt.title("Out-of-Sample Growth of $1 (10 bp one-way cost)")
    plt.ylabel("Growth of $1")
    plt.xlabel("")
    plt.grid(alpha=.25)
    plt.tight_layout()
    plt.savefig(OUTPUTS / "out_of_sample_growth.png", dpi=160)
    plt.close()

    daily_liquidity = {}
    for symbol in ASSETS:
        frame = yahoo_chart(symbol, "1d")
        frame = frame.loc[frame.index >= test.index.min()]
        daily_liquidity[symbol] = frame.volume * frame.close
    daily_dollar_volume = pd.concat(daily_liquidity, axis=1)
    liquidity = daily_dollar_volume.median().rename("median_daily_dollar_volume").to_frame()
    liquidity["fifth_percentile_daily_dollar_volume"] = daily_dollar_volume.quantile(.05)
    liquidity.to_csv(OUTPUTS / "liquidity_proxies.csv", index_label="asset")

    oas = pd.concat({"investment_grade_oas": fred_series("BAMLC0A0CM"), "high_yield_oas": fred_series("BAMLH0A0HYM2")}, axis=1)
    oas.to_csv(DATA / "fred_credit_oas_daily.csv", index_label="date")
    oas.describe(percentiles=[.05, .5, .95]).T.to_csv(OUTPUTS / "credit_spread_summary.csv", index_label="series")

    scenario = pd.DataFrame(SCENARIO_INPUTS).T
    scenario.to_csv(DATA / "scenario_duration_inputs.csv", index_label="asset")
    shock_defs = {
        "parallel_up_100bp": {"2y": .01, "5y": .01, "10y": .01, "30y": .01, "ig_spread": 0, "hy_spread": 0},
        "bear_steepener": {"2y": .0025, "5y": .005, "10y": .01, "30y": .0125, "ig_spread": .0025, "hy_spread": .0075},
        "credit_widening": {"2y": 0, "5y": 0, "10y": 0, "30y": 0, "ig_spread": .005, "hy_spread": .015},
    }
    srows = []
    for pname, w in weights.items():
        for shock, d in shock_defs.items():
            asset_impacts = []
            for asset in ASSETS:
                x = scenario.loc[asset]
                rate = sum(x[f"krd_{k}"] * d[k] for k in ["2y", "5y", "10y", "30y"])
                spread = x.spread_duration * (d["ig_spread"] if asset == "LQD" else d["hy_spread"] if asset == "HYG" else 0)
                asset_impacts.append(-(rate + spread))
            srows.append({"portfolio": pname, "scenario": shock, "estimated_price_impact": float(w @ np.array(asset_impacts))})
    pd.DataFrame(srows).to_csv(OUTPUTS / "duration_scenario_impacts.csv", index=False)

    summary = {
        "price_start": str(prices.index.min().date()), "price_end": str(prices.index.max().date()),
        "training_months": len(train), "test_months": len(test), "test_start": str(test.index.min().date()), "test_end": str(test.index.max().date()),
        "assets": ASSETS, "benchmark": BENCHMARK,
    }
    (OUTPUTS / "run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


if __name__ == "__main__":
    run()
