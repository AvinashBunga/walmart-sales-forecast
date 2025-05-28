# walmart-sales-forecast
End-to-end Walmart weekly sales forecast - Python | Tableau

Walmart Weekly Sales Forecast Project - 26 Weeks

Project Title: Learning from the Past: Reverse and Forward Forecasting of Walmart Weekly Sales

# Why Reverse Forecast?
To verify that the Prophet model accurately captures seasonal and holiday-driven peaks and troughs, a reverse forecast is performed on existing historical data (2010–2012). Overlaying the fitted forecast onto known sales confirms alignment with Christmas spikes and post‑holiday dips. Once validated, the forecast extends forward for the next 26 weeks.

**Data Source on Kaggle:**  
Walmart Weekly Sales Forecast Dataset: https://www.kaggle.com/datasets/mikhail1681/walmart-sales/data

# Sections
# Live Dashboard:
View the interactive forecast on Tableau Public - https://public.tableau.com/app/profile/avinash.bunga/viz/Walmart1_17481954405640/Dashboard3#1

# Overview
* Business problem and data sources
* Rationale for reverse forecasting

# Stage 1: Data Aggregation
* Inputs: raw daily sales + regressors (Holiday_Flag, Temperature, Fuel_Price, CPI, Unemployment)
* Output: stage1_national_walmart.csv with weekly granularity

# Stage 2: Prophet Forecasting
* Model setup: logistic growth, holiday effects, external regressors
* Hyperparameter tuning via back‑test CV
* Reverse forecast applied to 2010–2012 data
* Forward forecast generated for 26 weeks
* Outputs: stage2_tuned_forecast.csv (historical + future, with lower/upper bounds)

# Stage 3: Combine & Export
* Merge actuals vs. forecast
* Tag records as historical vs. forecast (IsForecast) and holidays (Holiday_Flag)
* Output: stage3_national_actual_vs_forecast.csv

# Tableau Dashboard
* Dual‑axis visualization: actual vs. learned forecast
* Holiday markers highlighted
* Forecast ribbon illustrating prediction intervals for future dates

# Usage Instructions
* Command‑line script execution order
* Steps to refresh data in Tableau

# Key Insights
* Back‑test MAPE and tuning results
* Model accuracy on holiday peaks

# Appendix
* Code snippets and configuration
* Environment setup and dependencies
