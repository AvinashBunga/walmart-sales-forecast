#!/usr/bin/env python3
import os, sys
import pandas as pd

def main():
    base     = os.path.dirname("/Users/avinash/Desktop/CIS/Avinash/MERSEA/Walmart1/Walmart_Sales.csv")
    hist_fp  = os.path.join(base, "stage1_national_walmart.csv")
    fcast_fp = os.path.join(base, "stage2_forced_holiday_plus_forecast.csv")
    out_fp   = os.path.join(base, "stage3_national_actual_vs_forecast.csv")

    # Load
    actuals  = pd.read_csv(hist_fp,  parse_dates=["Week"])
    forecast = pd.read_csv(fcast_fp, parse_dates=["Week"])

    # Merge & flag
    df = pd.merge(actuals, forecast, on="Week", how="outer", sort=True)
    last_hist = actuals.Week.max()
    df["IsForecast"] = (df.Week > last_hist).astype(int)

    # Ensure Holiday_Flag exists
    if "Holiday_Flag" not in df:
        df["Holiday_Flag"] = 0
    df["Holiday_Flag"] = df["Holiday_Flag"].fillna(0).astype(int)

    # Select + reorder
    df = df[[
        "Week",
        "Sales_Units",
        "Forecast_Units",
        "Forecast_Lower",
        "Forecast_Upper",
        "Holiday_Flag",
        "IsForecast"
    ]]

    # Save
    df.to_csv(out_fp, index=False)

    # Summary
    total     = len(df)
    hist_cnt  = int((df.IsForecast == 0).sum())
    fcast_cnt = int((df.IsForecast == 1).sum())
    hol_cnt   = int(df.Holiday_Flag.sum())
    print(f"\nStage 3 complete — wrote: {out_fp}")
    print(f" • Total weeks       : {total}")
    print(f" • Historical rows   : {hist_cnt}  (IsForecast=0)")
    print(f" • Forecast rows     : {fcast_cnt}  (IsForecast=1)")
    print(f" • Holiday weeks     : {hol_cnt}  (Holiday_Flag=1)\n")
    print("Last 5 rows:\n", df.tail(5).to_string(index=False))

if __name__=="__main__":
    main()
