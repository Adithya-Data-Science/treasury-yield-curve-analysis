from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SERIES = {"DGS2":"2Y", "DGS5":"5Y", "DGS10":"10Y", "DGS30":"30Y"}

def load_series(code):
    url=f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={code}"
    df=pd.read_csv(url)
    date_column=df.columns[0]
    df=df.rename(columns={date_column:"DATE",code:SERIES[code]})
    df["DATE"]=pd.to_datetime(df["DATE"],errors="coerce")
    df[SERIES[code]]=pd.to_numeric(df[SERIES[code]], errors="coerce")
    return df

def derive(df):
    x=df.dropna(subset=list(SERIES.values())).copy()
    x["level"]=x[list(SERIES.values())].mean(axis=1)
    x["slope_10y_2y"]=x["10Y"]-x["2Y"]
    x["slope_30y_2y"]=x["30Y"]-x["2Y"]
    x["curvature_5y"]=2*x["5Y"]-x["2Y"]-x["10Y"]
    x["curve_shape"]=x["slope_10y_2y"].apply(lambda v:"inverted" if v<0 else "positive")
    return x

def main():
    out=ROOT/"outputs"; out.mkdir(exist_ok=True)
    df=None
    for code in SERIES:
        s=load_series(code)
        df=s if df is None else df.merge(s,on="DATE",how="outer")
    result=derive(df.sort_values("DATE"))
    result.to_csv(out/"yield_curve_measures.csv",index=False)
    result["curve_shape"].value_counts().rename_axis("shape").to_csv(out/"shape_counts.csv")
    ax=result.plot(x="DATE",y="slope_10y_2y",title="U.S. Treasury 10Y-2Y slope",legend=False)
    ax.axhline(0,color="black",linewidth=.8); ax.set_ylabel("Percentage points")
    plt.tight_layout(); plt.savefig(out/"slope.png",dpi=160); plt.close()
    print(result.tail().to_string(index=False))
if __name__=="__main__": main()
