"""Walk-forward fixed-income ETF portfolio study.

Uses month-end adjusted-price series for SHY, IEF, TLT, LQD, and HYG.
The committed data are a static research snapshot; see README for provenance.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize

ASSETS = ["SHY", "IEF", "TLT", "LQD", "HYG"]
CAP = 0.45
TRAIN_MONTHS = 60
REBALANCE_MONTHS = 12
TRADING_COST = 0.001
DATA = Path(__file__).parent / "data" / "monthly_adjusted_prices.csv"
OUTPUT = Path(__file__).parent / "outputs"


def min_volatility_weights(returns: pd.DataFrame) -> np.ndarray:
    covariance = returns.cov().to_numpy() * 12
    n_assets = covariance.shape[0]

    def volatility(weights: np.ndarray) -> float:
        return float(np.sqrt(weights @ covariance @ weights))

    result = minimize(
        volatility,
        np.repeat(1 / n_assets, n_assets),
        method="SLSQP",
        bounds=[(0.0, CAP)] * n_assets,
        constraints={"type": "eq", "fun": lambda weights: weights.sum() - 1},
        options={"ftol": 1e-12, "maxiter": 2_000},
    )
    if not result.success:
        raise RuntimeError(result.message)
    return result.x


def annualized_metrics(returns: pd.Series, benchmark: pd.Series) -> dict[str, float]:
    aligned = pd.concat([returns.rename("portfolio"), benchmark.rename("benchmark")], axis=1).dropna()
    portfolio = aligned["portfolio"]
    active = portfolio - aligned["benchmark"]
    years = len(portfolio) / 12
    annual_return = (1 + portfolio).prod() ** (1 / years) - 1
    annual_volatility = portfolio.std(ddof=1) * np.sqrt(12)
    tracking_error = active.std(ddof=1) * np.sqrt(12)
    information_ratio = active.mean() * 12 / tracking_error
    wealth = (1 + portfolio).cumprod()
    max_drawdown = (wealth / wealth.cummax() - 1).min()
    return {
        "observations": len(portfolio),
        "annual_return": annual_return,
        "annual_volatility": annual_volatility,
        "tracking_error": tracking_error,
        "information_ratio": information_ratio,
        "max_drawdown": max_drawdown,
    }


def run() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    prices = pd.read_csv(DATA, parse_dates=["Date"], index_col="Date")[ASSETS]
    returns = prices.pct_change(fill_method=None).dropna()
    portfolio_returns: list[pd.Series] = []
    weight_rows: list[pd.Series] = []
    turnovers: list[float] = []
    previous = np.zeros(len(ASSETS))

    for start in range(TRAIN_MONTHS, len(returns), REBALANCE_MONTHS):
        train = returns.iloc[start - TRAIN_MONTHS : start]
        test = returns.iloc[start : start + REBALANCE_MONTHS]
        if test.empty:
            continue
        weights = min_volatility_weights(train)
        turnover = float(np.abs(weights - previous).sum())
        period = test @ weights
        period.iloc[0] -= turnover * TRADING_COST
        portfolio_returns.append(period)
        weight_rows.append(pd.Series(weights, index=ASSETS, name=test.index[0]))
        turnovers.append(turnover)
        previous = weights

    portfolio = pd.concat(portfolio_returns).sort_index().rename("portfolio_return")
    weights = pd.DataFrame(weight_rows)
    metrics = annualized_metrics(portfolio, returns.loc[portfolio.index, "LQD"])
    metrics["annual_turnover"] = float(np.mean(turnovers))
    metrics["annual_transaction_cost"] = metrics["annual_turnover"] * TRADING_COST
    metrics["history_start"] = str(prices.index.min().date())
    metrics["history_end"] = str(prices.index.max().date())
    metrics["history_months"] = len(prices)

    OUTPUT.mkdir(exist_ok=True)
    portfolio.to_csv(OUTPUT / "out_of_sample_returns.csv")
    weights.to_csv(OUTPUT / "rebalance_weights.csv", index_label="Date")
    pd.Series(metrics, name="value").to_csv(OUTPUT / "summary_metrics.csv")
    return prices, weights, metrics


if __name__ == "__main__":
    _, _, summary = run()
    for key, value in summary.items():
        print(f"{key}: {value}")
