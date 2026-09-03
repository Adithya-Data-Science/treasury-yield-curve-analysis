# U.S. Treasury Yield-Curve Analysis

Reproducible analysis of daily 2Y, 5Y, 10Y and 30Y constant-maturity Treasury yields from FRED. The pipeline calculates level (mean yield), slope (10Y-2Y), long slope (30Y-2Y) and curvature (2x5Y-2Y-10Y), classifies curve shape and produces summary tables and charts.

Run `pip install -r requirements.txt` then `python src/analyze.py`. The script records the retrieval date and source URLs. Tests use a fixed fixture and require no network access.

Interpretation is descriptive, not investment advice. FRED series can be revised and missing business-day observations are retained as missing until rows with incomplete maturities are excluded.

