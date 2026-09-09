import numpy as np
import pandas as pd

from src.analyze import annual_metrics, optimize_weights, turnover_cost_returns


def test_weights_sum_and_cap():
    rng = np.random.default_rng(7)
    returns = pd.DataFrame(rng.normal(.004, .02, (120, 5)))
    for objective in ["min_vol", "max_sharpe"]:
        w = optimize_weights(returns, objective)
        assert np.isclose(w.sum(), 1)
        assert (w >= -1e-9).all()
        assert (w <= .45 + 1e-9).all()


def test_costs_cannot_raise_returns():
    returns = pd.DataFrame([[.01, -.01], [-.02, .03]], columns=["a", "b"])
    w = np.array([.5, .5])
    assert (turnover_cost_returns(returns, w, 10) <= turnover_cost_returns(returns, w, 0)).all()


def test_tracking_error_zero_for_identical_series():
    r = pd.Series([.01, -.02, .03, .005])
    assert np.isclose(annual_metrics(r, r)["tracking_error"], 0)

