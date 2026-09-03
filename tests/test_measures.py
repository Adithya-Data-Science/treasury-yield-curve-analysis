import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).parents[1]/"src"))
from analyze import derive
def test_curve_measures():
    x=derive(pd.DataFrame({"DATE":["2026-01-01"],"2Y":[4.0],"5Y":[3.8],"10Y":[3.5],"30Y":[4.2]}))
    assert x.iloc[0]["slope_10y_2y"] == -0.5
    assert abs(x.iloc[0]["curvature_5y"]-0.1)<1e-9
    assert x.iloc[0]["curve_shape"] == "inverted"

