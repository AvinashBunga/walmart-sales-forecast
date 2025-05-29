#!/usr/bin/env python3
import os, sys
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
from dateutil.easter import easter

def main():
    #1. Paths
    base     = os.path.dirname("/Users/avinash/Desktop/CIS/Avinash/MERSEA/Walmart1/Walmart_Sales.csv")
    inp      = os.path.join(base, "stage1_national_walmart.csv")
    out_fp   = os.path.join(base, "stage2_forced_holiday_plus_forecast.csv")

    #2. Load & Prep
    try:
        df = pd.read_csv(inp, parse_dates=["Week"])
    except FileNotFoundError:
        sys.exit(f"ERROR: cannot find {inp}")
    df.rename(columns={"Week":"ds","Sales_Units":"y"}, inplace=True)

    # logistic cap 10% above max sales
    cap = df.y.max() * 1.1
    df["cap"] = cap

    # build forced-event table: Christmas, Post‐Xmas, BlackFriday, Easter
    years = list(range(df.ds.dt.year.min(), df.ds.dt.year.max()+3))
    events = []
    for y in years:
        events += [
            {"holiday":"Christmas",    "ds":pd.to_datetime(f"{y}-12-24"), "lower_window":-1, "upper_window":2},
            {"holiday":"PostChristmas","ds":pd.to_datetime(f"{y}-12-31"), "lower_window": 0, "upper_window":1},
            {"holiday":"BlackFriday",  "ds":pd.to_datetime(f"{y}-11-26"), "lower_window": 0, "upper_window":0},
            {"holiday":"Easter",       "ds":easter(y),                   "lower_window": 0, "upper_window":0},
        ]
    holidays_df = pd.DataFrame(events)

    #3. Build & Fit Prophet
    m = Prophet(
        growth="logistic",
        holidays=holidays_df,
        seasonality_mode="multiplicative",
        yearly_seasonality=False,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.1,
        holidays_prior_scale=500.0,
        seasonality_prior_scale=5.0
    )
    m.add_seasonality(name="annual", period=365.25, fourier_order=25)

    m.fit(df[["ds","y","cap"]])

    #4. Back-test CV
    print("🔍 Back-testing (365d train → 180d test)…")
    df_cv = cross_validation(
        m,
        initial="365 days",
        period="90 days",
        horizon="180 days",
        parallel="threads"
    )
    pm   = performance_metrics(df_cv)
    mape = pm.loc[pm.horizon=="180 days","mape"].mean()
    print(f"👉 Back-test MAPE: {mape:.2%}")
    if mape > 0.10:
        print(f"⚠️  MAPE {mape:.2%} > 10% — consider tuning further")

    #5. Forecast next 26 weeks
    future = m.make_future_dataframe(periods=26, freq="W-MON")
    future["cap"] = cap
    forecast = m.predict(future)

    #6. Save forecast
    out = forecast[["ds","yhat","yhat_lower","yhat_upper"]].rename(columns={
        "ds":"Week",
        "yhat":"Forecast_Units",
        "yhat_lower":"Forecast_Lower",
        "yhat_upper":"Forecast_Upper"
    })
    out.to_csv(out_fp, index=False)

    print(f"\n✅ Stage 2 complete — wrote: {out_fp}")
    print(f" • Total rows    : {len(out)}")
    print(f" • In-sample     : {len(df)}")
    print(f" • Forecast rows : {len(out) - len(df)}")

if __name__=="__main__":
    from multiprocessing import freeze_support
    freeze_support()
    main()
