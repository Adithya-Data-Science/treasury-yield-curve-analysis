from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parent

ASSETS = ["Short Treasury", "Intermediate Treasury", "TIPS", "IG Credit", "High Yield"]
EXPECTED_RETURNS = np.array([0.035, 0.045, 0.043, 0.055, 0.068])
VOLATILITIES = np.array([0.025, 0.060, 0.055, 0.075, 0.120])
CORRELATION = np.array([
    [1.00, 0.65, 0.45, 0.25, 0.05],
    [0.65, 1.00, 0.60, 0.45, 0.15],
    [0.45, 0.60, 1.00, 0.35, 0.10],
    [0.25, 0.45, 0.35, 1.00, 0.65],
    [0.05, 0.15, 0.10, 0.65, 1.00],
])
RISK_FREE = 0.03
MAX_WEIGHT = 0.45


def covariance_matrix() -> np.ndarray:
    return np.outer(VOLATILITIES, VOLATILITIES) * CORRELATION


def portfolio_metrics(weights: np.ndarray, covariance: np.ndarray) -> dict[str, float]:
    expected_return = float(weights @ EXPECTED_RETURNS)
    volatility = float(np.sqrt(weights @ covariance @ weights))
    sharpe = (expected_return - RISK_FREE) / volatility
    return {"expected_return": expected_return, "volatility": volatility, "sharpe": sharpe}


def optimize(objective, covariance: np.ndarray) -> np.ndarray:
    count = len(ASSETS)
    result = minimize(
        objective,
        np.repeat(1 / count, count),
        method="SLSQP",
        bounds=[(0, MAX_WEIGHT)] * count,
        constraints=[{"type": "eq", "fun": lambda w: np.sum(w) - 1}],
    )
    if not result.success:
        raise RuntimeError(result.message)
    return result.x


def main() -> None:
    covariance = covariance_matrix()
    equal = np.repeat(1 / len(ASSETS), len(ASSETS))
    min_vol = optimize(lambda w: portfolio_metrics(w, covariance)["volatility"], covariance)
    max_sharpe = optimize(lambda w: -portfolio_metrics(w, covariance)["sharpe"], covariance)

    output = {
        "status": "illustrative_client_scenario",
        "assumptions": {
            "assets": ASSETS,
            "expected_returns": EXPECTED_RETURNS.tolist(),
            "volatilities": VOLATILITIES.tolist(),
            "risk_free_rate": RISK_FREE,
            "maximum_asset_weight": MAX_WEIGHT,
        },
        "portfolios": {},
    }
    for name, weights in {"equal_weight": equal, "minimum_volatility": min_vol, "maximum_sharpe": max_sharpe}.items():
        output["portfolios"][name] = {
            "weights": dict(zip(ASSETS, map(float, weights))),
            **portfolio_metrics(weights, covariance),
        }

    output_path = ROOT / "reference_results.json"
    output_path.write_text(json.dumps(output, indent=2))
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
