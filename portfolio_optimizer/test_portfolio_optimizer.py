import numpy as np
import pandas as pd

from analysis import CAP, ASSETS, min_volatility_weights


def test_weights_respect_constraints():
    rng = np.random.default_rng(7)
    returns = pd.DataFrame(rng.normal(0.003, 0.02, (120, len(ASSETS))), columns=ASSETS)
    weights = min_volatility_weights(returns)
    assert np.isclose(weights.sum(), 1.0)
    assert np.all(weights >= -1e-9)
    assert np.all(weights <= CAP + 1e-9)
