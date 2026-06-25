# Retail Sales Optimization — Final Report
## ABC Retail Corp | Data Engineering Capstone

**Team 2** 

| Student ID | Name |
|------------|------|
| G25AI1006 | Amandeep |
| G25AI1007 | Amitesh Srivastava |
| G25AI1008 | Ananya Basu |
| G25AI1009 | Anbu Karthika Durairaj |
| G25AI1010 | Aniket |

---

## Executive Summary

Team 2 built an end-to-end data engineering pipeline for ABC Retail Corp using the Rossmann Store Sales dataset — 1,017,209 transactions across 1,115 stores spanning January 2013 to July 2015. The project delivers a fully automated ETL pipeline, a star schema data warehouse, a 37-feature engineered dataset, and a Random Forest sales forecasting model achieving **13.16% RMSPE** — comfortably below the 15% industry benchmark. Key findings include a 39.1% sales uplift from promotions, Friday as the peak sales day, and Store 262 as the top-performing outlet at €1.97M in predicted revenue.

---

## Project Timeline

| Week | Phase | Deliverable |
|------|-------|-------------|
| 1 | Data inventory | Data inventory report + quality assessment |
| 2 | Data cleaning | rossmann_cleaned.csv (844,338 rows) + cleaning log |
| 3 | ETL pipeline | Automated Python pipeline + timestamped log files |
| 4 | Schema + features | SQLite star schema + 37-feature dataset |
| 5 | Modeling | Random Forest model, RMSPE 13.16% + evaluation report |
| 6 | Dashboard + reporting | 5 visualizations + final report + presentation slides |

---

## Dataset Overview

| Property | Value |
|----------|-------|
| Source | Rossmann Store Sales (Kaggle) |
| Raw training rows | 1,017,209 |
| Store records | 1,115 |
| Date range | January 2013 – July 2015 |
| Files used | train.csv, store.csv |
| Rows after cleaning | 844,338 (open days only) |
| Final engineered features | 37 columns |

---

## Technical Architecture

```
data/raw/  (train.csv, store.csv)
     │
     ▼
pipeline/extract.py      ── typed CSV loading with date parsing
     │
     ▼
pipeline/transform.py    ── cleaning, anomaly fixes, merging
     │
     ▼
pipeline/load.py         ── saves to data/processed/
     │
     ▼
SQLite star schema        ── fact_sales + dim_date + dim_store + dim_promo
     │
     ▼
Feature engineering       ── 37 features: lags, rolling averages, encodings
     │
     ▼
Random Forest Regressor   ── trained Jan 2013 – Apr 2015
     │
     ▼
Sales forecasts           ── May – Jul 2015, per store per day
```

The entire pipeline runs end-to-end with a single command:

```bash
python pipeline/run_pipeline.py
```

Execution time: approximately 15 seconds. Every run produces a timestamped log file in `logs/` for auditability.

---

## Phase 1 — Data Inventory and Quality Assessment (Weeks 1–2)

### Week 1: Data Inventory

Three files were downloaded from Kaggle and loaded into the analysis environment:

- `train.csv` — 1,017,209 rows × 9 columns, date range Jan 2013–Jul 2015
- `store.csv` — 1,115 rows × 10 columns, one record per store
- `test.csv` — held out, not used in analysis

Initial profiling confirmed zero missing values in train.csv and zero duplicate rows. All columns loaded with correct types after applying `dtype={'StateHoliday': str}` and `parse_dates=['Date']`.

### Week 2: Data Cleaning

#### Missing Values Resolved

| Column | Missing Count | Fix Applied | Reasoning |
|--------|--------------|-------------|-----------|
| CompetitionDistance | 3 | Median imputation | Small count, median preserves distribution |
| CompetitionOpenSinceMonth | 354 | Filled with 0 | No competitor opening date known |
| CompetitionOpenSinceYear | 354 | Filled with 0 | Same as above |
| Promo2SinceWeek | 544 | Filled with 0 | Store not enrolled in Promo2 program |
| Promo2SinceYear | 544 | Filled with 0 | Same as above |
| PromoInterval | 544 | Filled with 'None' | Same as above |

#### Anomalies Resolved

| Issue | Count | Resolution |
|-------|-------|------------|
| StateHoliday mixed int/string types | All rows | Standardized to string: 'none', 'a', 'b', 'c' |
| Open=1 but Sales=0 | 54 rows | Corrected Open flag to 0 |
| Closed store days (Open=0) | 172,871 rows | Excluded — not relevant to sales forecasting |

#### Outlier Analysis

Sales IQR range: approximately −392 to 13,812. Outliers (3.64% of rows, ~30,769) were retained as they represent genuine high-sales events valuable for forecasting accuracy.

**Final cleaned dataset:** 844,338 rows × 18 columns saved to `data/processed/rossmann_cleaned.csv`.

---

## Phase 2 — ETL Pipeline and Data Ingestion (Week 3)

### Pipeline Architecture

The automated ingestion pipeline is structured as three independent Python modules under `pipeline/`:

| Module | Responsibility |
|--------|---------------|
| `extract.py` | Loads raw CSVs from `data/raw/` with correct dtypes and date parsing |
| `transform.py` | Applies all cleaning logic as named, reusable functions |
| `load.py` | Saves processed output to `data/processed/` |
| `run_pipeline.py` | Orchestrates all steps with dual console + file logging |

### Logging

Every pipeline run produces a timestamped log file:

```
2026-06-26 00:12:03 - INFO - === Pipeline started ===
2026-06-26 00:12:04 - INFO - Train extracted: (1017209, 9)
2026-06-26 00:12:04 - INFO - Store extracted: (1115, 10)
2026-06-26 00:12:04 - INFO - Store cleaned. Nulls remaining: 0
2026-06-26 00:12:04 - INFO - Train cleaned. Open days only: 844338
2026-06-26 00:12:04 - INFO - Merged shape: (844338, 18), Nulls: 0
2026-06-26 00:12:06 - INFO - Saved 844338 rows to rossmann_cleaned.csv
2026-06-26 00:12:06 - INFO - === Pipeline complete ===
```

---

## Phase 2 — Schema Design and Feature Engineering (Week 4)

### Star Schema Design

A star schema was designed and stored in SQLite (`rossmann_warehouse.db`):

```
                      ┌──────────────┐
                      │  fact_sales   │
                      │  844,338 rows │
                      └──────┬───────┘
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
      ┌──────────┐    ┌───────────┐    ┌──────────┐
      │ dim_date  │    │ dim_store  │    │dim_promo │
      │ 942 rows  │    │ 1,115 rows │    │  23 rows │
      └──────────┘    └───────────┘    └──────────┘
```

### Query Optimizations

Three indexes were created to optimize common query patterns:

| Index name | Column indexed | Query type accelerated |
|------------|---------------|----------------------|
| idx_sales_store | fact_sales(Store) | Store-level aggregations |
| idx_sales_date | fact_sales(Date) | Time-range filtering |
| idx_sales_promo | fact_sales(Promo) | Promotion analysis |

### Feature Engineering

37 features were engineered from the base 18 columns:

| Group | Features Created | Business Purpose |
|-------|-----------------|-----------------|
| Time | Year, Month, Week, DayOfMonth, Quarter, IsWeekend | Capture seasonality and weekly cycles |
| Lag | Sales_Lag7, Sales_Lag14, Sales_Lag30 | Recent sales history for the model |
| Rolling average | Sales_MA7, Sales_MA30 | Short-term and long-term trend signals |
| Store aggregate | Store_AvgSales, Store_StdSales | Store baseline and volatility |
| Encoded categorical | StoreType_enc, Assortment_enc, StateHoliday_enc | ML-ready category representation |
| Competition | CompetitionDistance_log, HasCompetition | Competitive pressure indicators |
| Interaction | Promo_Weekend | Combined effect of promotions on weekends |

Note: Lag features used `.shift(1)` inside rolling calculations to prevent data leakage — ensuring no future sales information is visible to the model during training.

**Final engineered dataset:** 844,338 rows × 37 columns saved to `data/processed/rossmann_features.csv`.

---

## Phase 3 — Modeling (Week 5)

### Model Selection

Random Forest Regressor was selected over linear regression for the following reasons:

- Handles non-linear relationships between features and sales
- No feature scaling required
- Naturally handles interactions between features
- Provides feature importance scores directly
- Robust to outliers in the target variable

### Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| n_estimators | 100 | Balance between accuracy and training time |
| max_depth | 15 | Prevents overfitting on 800k+ rows |
| min_samples_leaf | 10 | Ensures stable leaf predictions |
| n_jobs | −1 | Uses all available CPU cores |
| random_state | 42 | Reproducibility |

### Train/Test Split

A time-based split was used to prevent data leakage:

| Set | Date Range | Rows |
|-----|-----------|------|
| Training | January 2013 – April 2015 | ~790,000 |
| Test | May 2015 – July 2015 | ~54,000 |

Random splitting was deliberately avoided — it would allow the model to train on future dates and produce inflated accuracy scores.

### Evaluation Results

| Metric | Value | Interpretation |
|--------|-------|----------------|
| MAE | 718.74 | Average absolute error per store per day in sales units |
| RMSE | 1,068.83 | Error metric that penalises large deviations more |
| RMSPE | **13.16%** | Official Rossmann metric — below the 15% target |

### Feature Importance

| Rank | Feature | Importance Score | Interpretation |
|------|---------|-----------------|----------------|
| 1 | Sales_MA30 | 0.49 | 30-day moving average is the dominant signal |
| 2 | Promo | 0.12 | Promotions have the largest single-day impact |
| 3 | Store_AvgSales | 0.09 | Store baseline strongly predicts future sales |
| 4 | DayOfWeek | 0.07 | Weekly shopping patterns are consistent |
| 5 | Sales_MA7 | 0.05 | Short-term momentum adds additional signal |

Forecast saved to `data/processed/sales_forecast.csv` with actual and predicted values per store per day.

---

## Phase 3 — Dashboard and Insights (Week 6)

Five visualizations were produced and saved to `reports/`:

| Chart | File | Key finding |
|-------|------|-------------|
| Monthly sales trend | dashboard_monthly_trend.png | Clear seasonality with Dec/Jan peaks |
| Sales by day of week | dashboard_day_of_week.png | Friday peak (8,174), Sunday lowest (3,136) |
| Promo impact | dashboard_promo_impact.png | 39.1% uplift on promotion days |
| Actual vs predicted (top 5 stores) | dashboard_forecast_top5.png | Model tracks weekly patterns accurately |
| Store type heatmap | dashboard_heatmap_storetype.png | Type 'b' consistently highest across all months |

---

## Key Business Insights

### 1. Promotions drive 39.1% more sales
Stores running a promotion averaged **39.1% higher daily sales** than non-promotion days. With 1,115 stores, this represents a substantial revenue lever. Promotions should be deployed strategically at stores with below-average Sales_MA30 to maximise incremental impact.

### 2. Friday is the peak day — Sunday is the trough
Average daily sales peak on **Friday at 8,174 units** and hit their lowest on **Sunday at 3,136 units** — a 2.6× difference within a single week. Inventory replenishment, staffing, and logistics should be structured around this predictable weekly cycle.

### 3. Store type 'b' leads all categories
The store type heatmap shows type 'b' stores consistently outperforming types a, c, and d across every month in the dataset. Operational practices at type 'b' stores should be audited and replicated across the lower-performing store types.

### 4. Revenue is well-distributed across the network
The top 10 stores (led by Store 262 at €1.97M) account for **2.5% of total predicted revenue** (€15.3M out of €604.7M). This indicates a well-diversified store network with no dangerous revenue concentration — but also means performance improvements must be scaled broadly rather than focusing on a handful of flagship stores.

### 5. Seasonal peaks are predictable and significant
The monthly sales trend shows clear spikes in November and December consistent with holiday shopping behaviour. The model can generate reliable store-level forecasts for October procurement planning, reducing the risk of stockouts during peak weeks.

### 6. Long-term trend dominates all other signals
Sales_MA30 accounts for 49% of model importance — far more than any other feature. Stores with strong 30-day momentum continue to perform well. This means early intervention when a store's rolling average starts declining is critical to preventing sustained underperformance.

---

## Recommendations for ABC Retail Corp

### Immediate (0–30 days)
1. **Increase promotion frequency at underperforming stores** — The 39.1% uplift is consistent across store types. Stores with Sales_MA30 below the network median should receive priority promotion scheduling.
2. **Align Friday staffing and replenishment** — Peak demand on Fridays is predictable. Logistics schedules should be adjusted so inventory arrives Thursday, not Friday.

### Medium-term (1–3 months)
3. **Audit type 'b' store operations** — Identify the specific operational, locational, or assortment factors that drive type 'b' outperformance and create a replication playbook for type 'a', 'c', and 'd' stores.
4. **Build an October procurement model** — Use the pipeline to generate store-level October–December forecasts each September, enabling more accurate bulk inventory purchases ahead of the holiday peak.

### Long-term (3–6 months)
5. **Automate weekly forecasting** — Schedule `run_pipeline.py` to run every Monday morning via Windows Task Scheduler or cron. Operations teams receive fresh, store-level predictions each week with zero manual effort.
6. **Expand to product-level SKU forecasting** — The current model operates at store level. Adding SKU-level transaction data would enable precision inventory management and reduce both overstock and stockout costs.

---

## AI Tools Used

| Tool | How It Was Used |
|------|----------------|
| Claude (Anthropic) | Code review, debugging pipeline errors, report writing, cleaning strategy |
| GitHub Copilot | Autocomplete for ETL scripts, SQL index syntax, transformation functions |
| ChatGPT | Brainstorming feature engineering ideas, explaining model selection trade-offs |

All AI assistance was used to augment the team's engineering work. Every AI suggestion was reviewed, tested, and validated before inclusion in the project. AI tool usage was documented throughout each weekly phase.

---

## Repository Structure

```
retail_project/
├── data/
│   ├── raw/                          ← original Rossmann CSV files (Kaggle)
│   └── processed/                    ← generated by pipeline (gitignored)
│       ├── rossmann_cleaned.csv
│       ├── rossmann_features.csv
│       └── sales_forecast.csv
├── pipeline/
│   ├── __init__.py
│   ├── extract.py                    ← data loading module
│   ├── transform.py                  ← cleaning and merging module
│   ├── load.py                       ← output saving module
│   └── run_pipeline.py               ← master orchestration script
├── notebooks/
│   ├── 01_data_inventory.ipynb       ← Week 1
│   ├── 02_data_cleaning.ipynb        ← Week 2
│   ├── 03_schema_and_features.ipynb  ← Week 4
│   ├── 04_modeling.ipynb             ← Week 5
│   └── 05_dashboard.ipynb            ← Week 6
├── reports/
│   ├── FINAL_REPORT.md               ← this document
│   ├── presentation.pdf
│   ├── week1_report.md
│   ├── week2_cleaning_log.md
│   ├── week3_pipeline_report.md
│   ├── week4_schema_report.md
│   ├── week5_model_report.md
│   ├── dashboard_monthly_trend.png
│   ├── dashboard_day_of_week.png
│   ├── dashboard_promo_impact.png
│   ├── dashboard_forecast_top5.png
│   └── dashboard_heatmap_storetype.png
├── logs/
│   └── pipeline_20260626_001203.log
├── .gitignore
└── README.md
```

---

## How to Reproduce This Project

```bash
# 1. Clone the repository
git clone https://github.com/Amitesh099/retail_project.git
cd retail_project

# 2. Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn sqlite3

# 3. Download Rossmann dataset from Kaggle and place in data/raw/
#    https://www.kaggle.com/c/rossmann-store-sales/data

# 4. Run the full pipeline
python pipeline/run_pipeline.py

# 5. Open notebooks in order (01 through 05) in Jupyter
jupyter notebook
```

---

*Team 2 | G25AI1006 · G25AI1007 · G25AI1008 · G25AI1009 · G25AI1010*
*Data Engineering Capstone Project*