# Week 5 Report — Predictive Modeling

## Problem Statement

The objective of Week 5 was to build a predictive model to forecast daily store-level sales for ABC Retail Corp using the cleaned and feature-engineered Rossmann Store Sales dataset.

The forecast output can support inventory planning, promotion planning, staffing decisions, and revenue estimation.

---

## Model Chosen

The selected model was:

```text
Random Forest Regressor
```

Random Forest was chosen because:

- It handles non-linear relationships well.
- It works effectively with tabular business data.
- It can use both numerical and encoded categorical features.
- It is robust to outliers.
- It provides feature importance values.
- It does not require heavy feature scaling.

---

## Target Variable

The target variable for prediction was:

```text
Sales
```

The model was trained to predict daily sales for each store.

---

## Train/Test Split

A time-based train/test split was used instead of a random split.

| Dataset | Period |
|---|---|
| Training data | January 2013 to April 2015 |
| Test data | May 2015 to July 2015 |

A time-based split was selected because this is a forecasting problem. Random splitting could allow future data patterns to leak into the training set, which would make the model result look unrealistically good.

---

## Model Results

| Metric | Value | Interpretation |
|---|---|---|
| MAE | 718.74 | On average, predictions were off by about 719 sales units |
| RMSE | 1068.83 | Larger errors were penalized more strongly |
| RMSPE | 13.16% | Percentage-based forecasting error |

The RMSPE value of 13.16% indicates that the model produced acceptable forecasting performance for a beginner-level retail sales forecasting pipeline.

---

## Important Features

The most useful features for prediction included:

| Feature | Business Meaning |
|---|---|
| Sales_Lag7 | Recent sales history from the previous week |
| Store_AvgSales | Average sales level of each store |
| Sales_MA7 | Short-term moving average trend |
| Sales_MA30 | Longer-term moving average trend |
| DayOfWeek | Weekly sales pattern |
| Promo | Promotion effect |
| StoreType | Store category effect |

These features helped the model understand store behavior, promotion impact, and time-based sales patterns.

---

## Business Insights

- Recent sales history is one of the strongest predictors of future sales.
- Stores with stronger historical average sales are likely to continue performing better.
- Promotions have a visible impact on sales and should be planned carefully.
- Weekly sales patterns are important for staffing and inventory planning.
- Forecasting output can help reduce stockout and overstock risk.

---

## Output Files

The modeling phase can generate the following output:

```text
data/processed/sales_forecast.csv
```

This file contains actual and predicted sales values and can be used in the dashboard for visual comparison.

If this file is not committed to GitHub, it can be regenerated from the modeling notebook.

---

## AI Tools Used

- ChatGPT was used for explanation, debugging support, and report refinement.
- GitHub Copilot was used for code completion support.
- Claude was used for documentation review.

All AI-generated suggestions were reviewed and validated before inclusion.

---

## Conclusion

Week 5 successfully implemented a sales forecasting model and documented the model results.

The Random Forest model provides useful forecasting support for inventory planning, promotion decisions, and sales performance monitoring.