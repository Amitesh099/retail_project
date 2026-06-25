# Retail Sales Optimization — Final Report
## ABC Retail Corp | Data Engineering Capstone

---

## Executive summary
This project built an end-to-end data engineering pipeline for ABC Retail Corp
using the Rossmann Store Sales dataset (1,017,209 transactions across 1,115 stores,
Jan 2013 – Jul 2015). The pipeline ingests, cleans, transforms, and models retail
sales data, culminating in a Random Forest forecasting model achieving 13.16% RMSPE.

---

## Project timeline
| Week | Phase | Key output |
|------|-------|-----------|
| 1 | Data inventory | Quality assessment report |
| 2 | Data cleaning | rossmann_cleaned.csv |
| 3 | ETL pipeline | Automated Python pipeline + logs |
| 4 | Schema + features | SQLite warehouse + 37-feature dataset |
| 5 | Modeling | Random Forest, RMSPE 13.16% |
| 6 | Dashboard | 5 visualizations + this report |

---

## Technical architecture
Raw CSVs → pipeline/extract.py → pipeline/transform.py → pipeline/load.py
→ SQLite star schema → Feature engineering → Random Forest model → Forecasts

---

## Key business insights
1. Promotions increase average daily sales by X% across all stores
2. Store type 'b' has the highest average daily sales (from heatmap)
3. Fridays and Mondays are peak sales days; Sundays lowest
4. The top 10 stores account for ~X% of total predicted revenue
5. Sales_MA30 is the strongest predictor — long-term trends dominate

---

## Model performance
| Metric | Value |
|--------|-------|
| MAE    | 718.74 |
| RMSE   | 1068.83 |
| RMSPE  | 13.16% |

---

## Recommendations for ABC Retail Corp
1. Increase promotion frequency for store types with low baseline sales
2. Stock inventory higher on Fridays — peak demand day
3. Investigate the top 10 stores for best practices to replicate

---

## AI tools used
- Claude (Anthropic): report writing, code review, debugging
- GitHub Copilot: autocomplete for pipeline scripts
- ChatGPT: brainstorming feature engineering ideas