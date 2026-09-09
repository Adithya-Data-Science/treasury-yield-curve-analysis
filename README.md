# Treasury Yield-Curve Regime & Time-Series Analysis

A reproducible fixed-income research project using daily U.S. Treasury constant-maturity yields from FRED. The workflow measures curve level, slope and curvature, classifies rate regimes and prepares the data for time-series and scenario analysis relevant to duration and portfolio positioning.

## Research question

How does the shape of the U.S. Treasury curve change across market regimes, and what do those changes imply for rate sensitivity and fixed-income portfolio analysis?

## Skills demonstrated

- Fixed-income and Treasury market analysis
- Yield-curve level, slope and curvature
- Time-series feature engineering
- Regime classification and scenario analysis
- Python, Pandas, Matplotlib and FRED data
- Reproducible research, validation and documentation

## Data

Daily FRED series:

- DGS2 - 2-Year Treasury yield
- DGS5 - 5-Year Treasury yield
- DGS10 - 10-Year Treasury yield
- DGS30 - 30-Year Treasury yield

## Start-to-finish workflow

1. Download daily Treasury constant-maturity yields directly from FRED.
2. Parse dates and coerce yield fields to numeric values.
3. Merge maturities into one aligned time-series dataset.
4. Retain only dates with complete observations across the selected maturities.
5. Calculate curve **level** as the mean yield across maturities.
6. Calculate **10Y-2Y slope** and **30Y-2Y long slope**.
7. Calculate **5Y curvature** as `2 x 5Y - 2Y - 10Y`.
8. Classify each observation as a positive or inverted 10Y-2Y curve regime.
9. Export machine-readable curve measures and regime counts.
10. Produce a time-series chart of the 10Y-2Y spread around the zero-inversion threshold.
11. Interpret results as descriptive rate-regime evidence, not as a standalone trading rule.

## Repository structure

```text
.
├── src/analyze.py
├── tests/
├── outputs/
│   ├── yield_curve_measures.csv
│   ├── shape_counts.csv
│   └── slope.png
├── requirements.txt
└── README.md
```

## Run

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/analyze.py
```

The pipeline records the current FRED observations at runtime, so results can update when the source data changes.

## What this project shows for quantitative research

The project converts raw market time series into economically interpretable state variables. Curve slope and curvature can be used as inputs to broader fixed-income models, scenario analysis or portfolio-risk studies, while the explicit data-cleaning and regime definitions make the analysis reproducible and auditable.

## Limitations

Treasury constant-maturity series are reference yields, not individual bond total returns. FRED observations can be revised, missing business-day values occur, and curve inversion alone does not establish a profitable investment strategy.

## Resume-ready description

**Treasury Yield-Curve Regime & Time-Series Analysis | Python, Pandas, FRED**

Built a reproducible daily Treasury research pipeline across 2Y, 5Y, 10Y and 30Y maturities; engineered curve level, slope and curvature measures, classified inversion regimes and exported time-series outputs for fixed-income scenario analysis. Documented missing-data handling, interpretation limits and the distinction between yield-curve signals and investable total-return evidence.
