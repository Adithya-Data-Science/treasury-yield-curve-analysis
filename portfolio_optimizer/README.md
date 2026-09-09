# Fixed-Income Portfolio Optimization and Client Analytics

This module constructs transparent allocations across Short Treasury, Intermediate Treasury, TIPS, investment-grade credit and high yield. It compares equal-weight, minimum-volatility and maximum-Sharpe portfolios subject to long-only weights, full investment and a 45% maximum position.

## Interpretation boundary

The inputs are an **illustrative client scenario**, not estimated historical performance and not an investment recommendation. Expected returns, volatilities and correlations are visible in the code and output so a reviewer can audit every assumption.

## Reproduce

```bash
pip install numpy scipy
python portfolio_optimizer.py
python -m unittest test_portfolio_optimizer.py
```

The run recreates `reference_results.json`, including weights, expected return, volatility and Sharpe ratio for every allocation.

## Workflow

1. Define five fixed-income exposures and explicit capital-market assumptions.
2. Convert volatility and correlation assumptions into a covariance matrix.
3. Apply long-only, fully invested and 45% concentration constraints.
4. Solve minimum-volatility and maximum-Sharpe allocations with SLSQP.
5. Compare both optimized portfolios with an equal-weight reference.
6. Validate covariance and allocation constraints with unit tests.

## Client use

The framework makes assumptions and tradeoffs visible for an asset-allocation discussion. A production study should replace the illustrative inputs with approved capital-market assumptions, add duration, spread, liquidity and liability constraints, and stress the solution across inflation and rate scenarios.

## Limitations

Mean-variance optimization is sensitive to expected returns and covariance estimates. The scenario omits estimation uncertainty, transaction costs, taxes, liquidity, tail dependence and regime shifts.
