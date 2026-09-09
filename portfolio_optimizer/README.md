# Historical Fixed-Income ETF Portfolio and Benchmark Analytics

This project constructs and evaluates a long-only minimum-volatility portfolio across five investable U.S.-listed bond ETFs: **SHY, IEF, TLT, LQD, and HYG**. LQD is used as the investment-grade corporate-bond benchmark.

## Research design

- Static adjusted-price snapshot covering January 2010 through December 2025
- Monthly total returns derived from adjusted prices
- 60-month trailing covariance-estimation window
- Annual portfolio rebalancing with a 45% per-ETF concentration cap
- Fully out-of-sample evaluation after each estimation window
- Turnover-based transaction costs of 10 basis points
- Benchmark-relative tracking error and information ratio versus LQD

The design deliberately separates every training window from its following holding period. Results are a historical research exercise, not expected future performance or investment advice.

## Reproduce

```bash
python -m pip install -r requirements.txt
python analysis.py
pytest -q
```

Generated files are written to `outputs/`:

- `summary_metrics.csv`
- `out_of_sample_returns.csv`
- `rebalance_weights.csv`

## Data provenance

The committed monthly snapshot was downloaded from Yahoo Finance's chart endpoint on September 9, 2026. Adjusted prices incorporate distributions and corporate actions. The snapshot is committed to make the analysis reproducible and to avoid changing results when an upstream service revises its history.

## Verified out-of-sample results

Across 131 out-of-sample monthly observations (February 2015-December 2025), the minimum-volatility strategy produced a 2.02% annualized return and 3.65% annualized volatility. Relative to LQD, it recorded 4.84% tracking error and a -0.14 information ratio. Average annual turnover was 14.6%, corresponding to approximately 0.01% annual modeled transaction cost at 10 basis points.

## Limitations

- ETF adjusted prices are investable proxies, not holdings-level bond returns.
- Optimization estimates remain sensitive to the selected window and universe.
- LQD is a practical benchmark for this study, not a universal benchmark for every mandate.
- Taxes, bid-ask spreads, market impact, and fund-management fees are not modeled separately.
