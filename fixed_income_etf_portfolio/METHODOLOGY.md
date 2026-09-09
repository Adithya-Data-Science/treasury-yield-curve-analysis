# Methodology and Limitations

## Research design

Monthly adjusted prices are aligned across SHY, IEF, TLT, LQD, HYG and AGG. Portfolio weights are estimated only from February 2010 through December 2018. The fixed January 2019 through August 2026 period is used once for out-of-sample evaluation.

The minimum-volatility and maximum-Sharpe allocations are long-only, fully invested and capped at 45% per sleeve. AGG is not eligible for the optimized portfolios; it is used only as the benchmark. Maximum Sharpe uses a zero risk-free rate so the calculation remains reproducible without mixing a separate cash series into the optimization.

## Risk and benchmark measures

- CAGR is the geometric annualized growth rate.
- Volatility is the monthly sample standard deviation multiplied by the square root of 12.
- Maximum drawdown is the lowest cumulative-wealth decline from a prior peak.
- Active return is the annualized arithmetic mean of portfolio return minus AGG return.
- Tracking error is the annualized sample standard deviation of monthly active return.
- Information ratio is annualized active return divided by tracking error.

## Costs and liquidity

Portfolios are returned to target weights monthly. One-way turnover equals half the absolute difference between post-return drifted weights and target weights. Net returns subtract turnover multiplied by 0, 5 or 10 basis points. This is a transparent sensitivity test, not a claim about executable institutional costs.

Liquidity is summarized using median and fifth-percentile daily dollar volume from closing price times reported volume during the test period. Dollar volume is a capacity proxy; it is not a bid-ask spread, market-impact model or guarantee of execution.

## Credit spreads

Credit context uses the ICE BofA U.S. Corporate Index option-adjusted spread and ICE BofA U.S. High Yield Index option-adjusted spread distributed through FRED. These series describe market-wide spread conditions and are not exact spread histories for LQD or HYG.

## Duration scenarios

The scenario file contains transparent, static research assumptions for rate duration, spread duration and 2Y/5Y/10Y/30Y key-rate contributions. They are applied through first-order duration approximations. The values are not historical holdings-based ETF exposures, and the estimates omit convexity, changing holdings, option effects, spread-rate interaction and trading responses.

The scenarios are:

- Parallel up 100 bp: every Treasury key rate rises 100 bp.
- Bear steepener: 2Y, 5Y, 10Y and 30Y rates rise 25, 50, 100 and 125 bp; investment-grade and high-yield spreads widen 25 and 75 bp.
- Credit widening: investment-grade and high-yield spreads widen 50 and 150 bp with Treasury rates unchanged.

## Limitations

- ETFs are investable proxies, not individual bonds or a complete institutional mandate.
- Adjusted-price quality depends on the upstream vendor and corporate-action treatment.
- One train/test split does not establish robustness across every market regime.
- Optimization is sensitive to estimated means and covariances.
- Static duration assumptions do not reproduce time-varying holdings-based risk.
- AGG may not be the correct benchmark for every investor or objective.
- Taxes, financing, management fees beyond adjusted-price treatment and detailed market impact are outside scope.

