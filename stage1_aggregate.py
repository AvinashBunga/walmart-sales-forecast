#!/usr/bin/env python3
import pandas as pd
import os
import sys

# ── 1. CONFIGURE PATHS ─────────────────────────────────────────────────────────
raw_path = "/Users/avinash/Desktop/CIS/Avinash/MERSEA/Walmart1/Walmart_Sales.csv"
out_path = os.path.join(os.path.dirname(raw_path), "stage1_national_walmart.csv")

# ── 2. LOAD RAW DATA ───────────────────────────────────────────────────────────
try:
    df = pd.read_csv(
        raw_path,
        parse_dates=["Date"],
        dayfirst=True,
        dtype={
            "Store": int,
            "Weekly_Sales": float,
            "Holiday_Flag": int,
            "Temperature": float,
            "Fuel_Price": float,
            "CPI": float,
            "Unemployment": float,
        }
    )
except FileNotFoundError:
    sys.exit(f"ERROR: could not find raw file at {raw_path}")

# ── 3. AGGREGATE BY WEEK ────────────────────────────────────────────────────────
#    We floor to the Monday of each week, then sum sales and carry regressors.
df["Week"] = df["Date"].dt.to_period("W").apply(lambda r: r.start_time)

weekly = (
    df.groupby("Week")
      .agg(
          Sales_Units   = ("Weekly_Sales", "sum"),
          Holiday_Flag  = ("Holiday_Flag",  "max"),
          Temperature   = ("Temperature",   "mean"),
          Fuel_Price    = ("Fuel_Price",    "mean"),
          CPI           = ("CPI",           "mean"),
          Unemployment  = ("Unemployment",  "mean"),
      )
      .reset_index()
)

# ── 4. SAVE AGGREGATION ────────────────────────────────────────────────────────
weekly.to_csv(out_path, index=False)

# ── 5. SUMMARY PRINT ───────────────────────────────────────────────────────────
total_weeks   = len(weekly)
first_week    = weekly["Week"].min().date()
last_week     = weekly["Week"].max().date()
holidays      = int(weekly["Holiday_Flag"].sum())
sales_err     = E = weekly["Sales_Units"]
print(f"\nStage 1 complete — wrote: {out_path}")
print(f" • Weeks         : {total_weeks}  ({first_week} → {last_week})")
print(f" • Holiday weeks : {holidays}")
print(f" • Sales_Units   : min={E.min():,.0f}, mean={E.mean():,.0f}, max={E.max():,.0f}")
print("\nSample:")
print(weekly.head().to_string(index=False))
