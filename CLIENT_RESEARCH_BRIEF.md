# Client Research Brief: Reading Treasury Curve Regimes

## Executive conclusion

The repository's stored dataset contains **12,382 complete daily observations**, of which **2,049 days (16.5%)** had a negative 10Y-2Y Treasury slope. The analysis converts 2Y, 5Y, 10Y, and 30Y constant-maturity yields into curve level, slope, curvature, and inversion-regime measures.

An inversion is useful as a macro-financial state variable, but it is not a standalone trading signal. Client decisions should combine the curve with inflation, growth, credit-spread, valuation, and portfolio-liability information.

## What changed across regimes

- **Level** summarizes the general rate environment and helps frame duration sensitivity.
- **10Y-2Y slope** distinguishes positive from inverted configurations.
- **30Y-2Y slope** provides a longer-horizon view of the term structure.
- **5Y curvature** captures how the intermediate maturity differs from a simple endpoint relationship.

## Scenario implications

| Scenario | Portfolio question | Analytical implication |
| --- | --- | --- |
| Bull steepening | Is duration exposure sufficient? | Falling front-end yields can benefit shorter and intermediate maturities while steepening the curve. |
| Bear steepening | Is long-duration risk controlled? | Rising long yields can pressure long-duration assets and increase rate volatility. |
| Bull flattening | How should gains be balanced with reinvestment risk? | Long yields may fall faster while front-end yields remain comparatively elevated. |
| Inversion | Is the portfolio relying on the curve as a timing signal? | Treat inversion as a regime indicator and test outcomes alongside macro and valuation variables. |

## Client use

The exported measures can support asset-allocation scenarios, duration discussions, stress testing, and features in broader forecasting models. They should not be translated directly into trades without total-return data, transaction costs, and forward-looking portfolio constraints.

## Limitations

Constant-maturity series are reference yields rather than individual bond total returns. FRED observations can be revised, missing dates occur, and the stored sample is descriptive. This brief is research documentation, not investment advice.
