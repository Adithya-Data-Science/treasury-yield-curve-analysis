import unittest

import numpy as np

from portfolio_optimizer import MAX_WEIGHT, covariance_matrix, optimize, portfolio_metrics


class PortfolioOptimizerTests(unittest.TestCase):
    def test_covariance_is_positive_semidefinite(self):
        self.assertGreaterEqual(np.linalg.eigvalsh(covariance_matrix()).min(), -1e-12)

    def test_optimizer_respects_allocation_constraints(self):
        covariance = covariance_matrix()
        weights = optimize(lambda w: portfolio_metrics(w, covariance)["volatility"], covariance)
        self.assertTrue(np.isclose(weights.sum(), 1.0))
        self.assertGreaterEqual(weights.min(), -1e-8)
        self.assertLessEqual(weights.max(), MAX_WEIGHT + 1e-8)


if __name__ == "__main__":
    unittest.main()
