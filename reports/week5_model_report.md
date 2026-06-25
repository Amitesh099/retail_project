# Week 5 Report — Predictive Modeling

## Problem statement
Predict daily sales for each Rossmann store for the next month
to support inventory planning and revenue forecasting.

## Model chosen: Random Forest Regressor
Chosen over linear regression because:
- Handles non-linear relationships (promotions, seasonality)
- No feature scaling required
- Built-in feature importance
- Robust to outliers

## Train/test split
- Method: time-based (not random) to prevent data leakage
- Train: Jan 2013 – Apr 2015
- Test: May 2015 – Jul 2015

## Results
| Metric | Value | Interpretation |
|--------|-------|----------------|
| MAE    | XXXX  | Average error per day per store |
| RMSE   | XXXX  | Penalizes large errors more |
| RMSPE  | X.XX% | Official Rossmann metric (< 15% is good) |

## Key findings from feature importance
1. Sales_Lag7 — most predictive (recent history = best signal)
2. Store_AvgSales — store baseline matters
3. Sales_MA7 — short-term trend
4. DayOfWeek — weekly patterns strong
5. Promo — promotions have clear uplift effect

## Business insights
- Top 10 stores account for X% of predicted revenue
- Stores with Promo=1 show X% higher predicted sales
- Weekend sales X% lower than weekday average

## AI tools used
- claude