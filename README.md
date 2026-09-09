# Treasury Yield-Curve Regime & Time-Series Analysis

A reproducible fixed-income study using daily U.S. Treasury constant-maturity yields from FRED. It turns raw 2Y, 5Y, 10Y and 30Y observations into curve level, slope, curvature and inversion-regime measures for portfolio and scenario analysis.

## Result snapshot

The stored output contains **12,382 complete daily observations**. The 10Y-2Y curve was inverted on **2,049 days (16.5%)** and positive on 10,333 days. These are descriptive regime statistics, not a standalone trading rule.

Read the [client research brief](CLIENT_RESEARCH_BRIEF.md) for rate scenarios, portfolio questions and interpretation limits.

## Research question

How does the shape of the U.S. Treasury curve change across market regimes, and what do those changes imply for rate sensitivity and fixed-income portfolio analysis?

## Data and measures

- FRED DGS2, DGS5, DGS10 and DGS30 daily series
- Curve level: mean yield across the four maturities
- 10Y-2Y and 30Y-2Y slopes
- 5Y curvature: `2 x 5Y - 2Y - 10Y`
- Positive versus inverted 10Y-2Y regimes

## Reproduce

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/analyze.py
pytest -q
```

The run downloads FRED observations, validates numeric fields and complete maturity rows, then recreates:

- `outputs/yield_curve_measures.csv` - analysis-ready time series
- `outputs/shape_counts.csv` - regime counts
- `outputs/slope.png` - 10Y-2Y history around the inversion threshold

## Start-to-finish workflow

1. Download each Treasury series directly from FRED.
2. Parse dates, coerce yields to numeric values and align maturities.
3. Retain observations complete across all four maturities.
4. Calculate level, short and long slopes, and intermediate curvature.
5. Classify inversion regimes with an explicit zero threshold.
6. Export data, counts and a time-series visualization.
7. Translate regimes into portfolio questions without presenting inversion as a trade.

## Repository map

- `src/analyze.py` - complete data and analytics pipeline
- `tests/test_measures.py` - unit validation for derived measures
- `outputs/` - stored evidence, chart and analysis-ready data
- `CLIENT_RESEARCH_BRIEF.md` - executive fixed-income interpretation
- `requirements.txt` - reproducible dependencies

## Limitations

Constant-maturity series are reference yields, not individual bond total returns. FRED observations can be revised, missing business-day values occur, and curve inversion alone does not establish a profitable investment strategy.
