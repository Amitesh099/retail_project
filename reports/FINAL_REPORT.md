# Retail Sales Optimization — Final Report

## ABC Retail Corp | Data Engineering Capstone

**Team 2**

| Student ID | Name |
|---|---|
| G25AI1006 | Amandeep |
| G25AI1007 | Amitesh Srivastava |
| G25AI1008 | Ananya Basu |
| G25AI1009 | Anbu Karthika Durairaj |
| G25AI1010 | Aniket |

---

## 1. Executive Summary

ABC Retail Corp is a retail business that wants to improve sales forecasting, promotion planning, and inventory decisions.

Team 2 developed a data engineering capstone project using the Rossmann Store Sales dataset. The project covers the complete beginner-friendly data engineering flow:

```text
Raw CSV data
→ Data quality check
→ Data cleaning
→ ETL pipeline
→ Transformed dataset
→ Feature engineering
→ Sales forecasting model
→ Visual dashboards
→ Business recommendations
```

The project uses Python, Pandas, Scikit-learn, Plotly, Streamlit, and Jupyter notebooks. The final output includes cleaned datasets, pipeline scripts, model evaluation, visual reports, and an interactive dashboard.

Live dashboard:

```text
https://capstone-retail-group2.streamlit.app/
```

The Random Forest forecasting model achieved the following results:

| Metric | Value |
|---|---|
| MAE | 718.74 |
| RMSE | 1068.83 |
| RMSPE | 13.16% |

The model result shows that store-level sales can be forecasted with reasonable accuracy using historical sales, promotion details, date-based features, and store-level information.

---

## 2. Business Problem

ABC Retail Corp wants to answer the following business questions:

- Which stores are performing well?
- How do promotions affect sales?
- Are there seasonal or monthly sales patterns?
- Which days of the week have higher sales?
- Can future sales be predicted?
- How can the business use these insights for inventory and promotion planning?

The purpose of this project is to convert raw retail data into useful business insights through a structured data engineering and analytics workflow.

---

## 3. Dataset Overview

The Rossmann Store Sales dataset was used for this project.

| Property | Value |
|---|---|
| Dataset | Rossmann Store Sales |
| Source | Kaggle |
| Main files used | `train.csv`, `store.csv` |
| Training rows | 1,017,209 |
| Store records | 1,115 |
| Date range | January 2013 to July 2015 |
| Final cleaned rows | 844,338 |
| Final cleaned columns | 18 |
| Final engineered features | 37 |

The raw dataset contains daily sales records for multiple stores, along with promotion, holiday, customer, and store-level information.

---

## 4. Project Timeline

| Week | Phase | Deliverable |
|---|---|---|
| Week 1 | Data inventory | Dataset selection, data inventory, initial quality assessment |
| Week 2 | Data cleaning | Cleaned dataset and cleaning log |
| Week 3 | ETL pipeline | Automated Python pipeline and logs |
| Week 4 | Schema and feature engineering | Star schema design and engineered dataset |
| Week 5 | Modeling | Random Forest sales forecasting model and evaluation report |
| Week 6 | Dashboard and reporting | Visual dashboard, final report, and presentation |

---

## 5. Technical Architecture

The project follows this architecture:

```text
data/raw/
  ├── train.csv
  ├── store.csv
  └── test.csv

        ↓

pipeline/extract.py
  Loads raw CSV files with correct datatypes and date parsing

        ↓

pipeline/transform.py
  Cleans missing values, fixes anomalies, and merges train/store data

        ↓

pipeline/load.py
  Saves cleaned output into data/processed/

        ↓

data/processed/rossmann_cleaned.csv

        ↓

Jupyter notebooks
  Schema design, feature engineering, modeling, and visualization

        ↓

reports/
  Weekly reports, charts, model results, and final report

        ↓

dashboard/app.py
  Interactive Streamlit dashboard
```

The core ETL pipeline runs with a single command and generates the cleaned merged dataset:

```bash
python pipeline/run_pipeline.py
```

This creates:

```text
data/processed/rossmann_cleaned.csv
```

Feature engineering, schema creation, modeling, and dashboard visualizations are performed through the notebooks in sequence.

---

## 6. Phase 1 — Data Inventory and Quality Assessment

### 6.1 Data Files Used

| File | Description |
|---|---|
| `train.csv` | Daily sales data for stores |
| `store.csv` | Store-level information |
| `test.csv` | Test dataset, kept for reference |

The project mainly uses `train.csv` and `store.csv`.

### 6.2 Initial Data Quality Checks

The following checks were performed:

- Number of rows and columns
- Missing values
- Duplicate records
- Datatype validation
- Date range validation
- Sales distribution
- Store-level coverage
- Holiday and promotion fields

### 6.3 Initial Observations

- `train.csv` contained more than 1 million sales records.
- `store.csv` contained 1,115 store records.
- The sales data covered the period from January 2013 to July 2015.
- Some store-level columns had missing values.
- Some stores were marked open but had zero sales.
- Closed store days were not useful for sales forecasting and were removed during cleaning.

---

## 7. Phase 2 — Data Cleaning

### 7.1 Cleaning Steps Performed

The following cleaning steps were applied:

| Issue | Action Taken |
|---|---|
| Missing `CompetitionDistance` | Filled using median value |
| Missing `CompetitionOpenSinceMonth` | Filled with 0 |
| Missing `CompetitionOpenSinceYear` | Filled with 0 |
| Missing `Promo2SinceWeek` | Filled with 0 |
| Missing `Promo2SinceYear` | Filled with 0 |
| Missing `PromoInterval` | Filled with `None` |
| Mixed `StateHoliday` values | Converted to string format |
| `Open = 1` but `Sales = 0` | Treated as anomaly and corrected |
| Closed store days | Removed from forecasting dataset |

### 7.2 Final Cleaned Dataset

After cleaning, the final dataset contained:

| Property | Value |
|---|---|
| Rows | 844,338 |
| Columns | 18 |
| Output file | `data/processed/rossmann_cleaned.csv` |

The cleaned dataset is used as the base input for further transformation, analysis, modeling, and dashboarding.

---

## 8. Phase 3 — ETL Pipeline

### 8.1 Pipeline Modules

The ETL pipeline is divided into modular Python files:

| File | Purpose |
|---|---|
| `pipeline/extract.py` | Reads raw CSV files |
| `pipeline/transform.py` | Cleans and merges data |
| `pipeline/load.py` | Saves processed output |
| `pipeline/run_pipeline.py` | Runs the full ETL pipeline |

### 8.2 Pipeline Flow

```text
extract.py
→ transform.py
→ load.py
→ run_pipeline.py
```

### 8.3 Pipeline Output

The pipeline creates the cleaned dataset:

```text
data/processed/rossmann_cleaned.csv
```

### 8.4 Logging

The pipeline generates timestamped logs inside the `logs/` folder. This helps track whether the pipeline completed successfully and supports auditability.

Example log flow:

```text
Pipeline started
Train data extracted
Store data extracted
Store data cleaned
Train data cleaned
Datasets merged
Cleaned CSV saved
Pipeline complete
```

---

## 9. Phase 4 — Schema Design and Feature Engineering

### 9.1 Star Schema Design

A simple star schema was designed for analytical storage.

```text
                 dim_store
                    |
dim_date ---- fact_sales ---- dim_promo
```

### 9.2 Fact Table

The fact table contains measurable business values.

| Table | Description |
|---|---|
| `fact_sales` | Daily sales records for stores |

Important columns:

- Store
- Date
- Sales
- Customers
- Promo
- Open
- StateHoliday
- SchoolHoliday

### 9.3 Dimension Tables

| Table | Description |
|---|---|
| `dim_store` | Store-level information |
| `dim_date` | Date, month, year, week, weekday information |
| `dim_promo` | Promotion and holiday-related information |

### 9.4 Feature Engineering

Feature engineering was performed to make the data suitable for forecasting.

Feature groups included:

| Feature Group | Examples |
|---|---|
| Date features | Year, Month, Week, DayOfWeek, Quarter |
| Weekend feature | IsWeekend |
| Lag features | Sales_Lag7, Sales_Lag14, Sales_Lag30 |
| Moving averages | Sales_MA7, Sales_MA30 |
| Store-level features | Store_AvgSales, Store_StdSales |
| Encoded categorical features | StoreType, Assortment, StateHoliday |
| Competition features | CompetitionDistance_log, HasCompetition |
| Interaction features | Promo_Weekend |

The final feature-engineered dataset contained 37 columns.

Output:

```text
data/processed/rossmann_features.csv
```

---

## 10. Phase 5 — Sales Forecasting Model

### 10.1 Model Selected

The project used a Random Forest Regressor for sales forecasting.

Random Forest was selected because:

- It can handle non-linear relationships.
- It works well with both numerical and encoded categorical features.
- It is robust for tabular business datasets.
- It provides feature importance.
- It does not require heavy feature scaling.

### 10.2 Target Variable

The model predicts:

```text
Sales
```

### 10.3 Train-Test Split

A time-based train-test split was used.

| Set | Period |
|---|---|
| Training data | Earlier historical sales records |
| Testing data | Later sales records |

A time-based split is better than random splitting for forecasting because it avoids training the model on future data.

### 10.4 Model Results

| Metric | Value | Meaning |
|---|---|---|
| MAE | 718.74 | Average absolute prediction error |
| RMSE | 1068.83 | Penalizes larger prediction errors |
| RMSPE | 13.16% | Percentage-based forecasting error |

### 10.5 Important Features

The strongest predictors included:

| Feature | Business Meaning |
|---|---|
| Sales_MA30 | Long-term sales trend |
| Promo | Promotion effect |
| Store_AvgSales | Store baseline performance |
| DayOfWeek | Weekly shopping pattern |
| Sales_MA7 | Short-term sales trend |

Forecast output:

```text
data/processed/sales_forecast.csv
```

---

## 11. Phase 6 — Dashboard and Visualizations

### 11.1 Static Visualizations

The following visualizations were created and saved in the `reports/` folder:

| Chart | Purpose |
|---|---|
| Monthly sales trend | Understand seasonality |
| Sales by day of week | Identify weekly sales pattern |
| Promotion impact | Compare promo vs non-promo sales |
| Actual vs predicted sales | Validate model output |
| Store type heatmap | Compare store type performance |

### 11.2 Interactive Dashboard Deployment

An interactive dashboard was developed using Streamlit and Plotly.

Dashboard file:

```text
dashboard/app.py
```

The dashboard includes:

- Date range filter
- Store filter
- Promotion filter
- KPI cards
- Daily sales trend
- Top 10 stores by sales
- Promotion impact analysis
- Monthly sales trend
- Forecast output section

Deployment platform:

```text
Streamlit Community Cloud
```

Live dashboard link:

```text
https://capstone-retail-group2.streamlit.app/
```

---

## 12. Key Business Insights

### 12.1 Promotions Increase Sales

Promotion days showed stronger sales performance compared with non-promotion days. This confirms that promotional campaigns are important for revenue growth.

### 12.2 Weekly Sales Pattern Exists

Sales vary by day of the week. This means staffing, inventory replenishment, and logistics can be planned based on expected weekly demand.

### 12.3 Store-Level Performance Varies

Some stores consistently perform better than others. Store-level analysis helps identify high-performing and low-performing stores.

### 12.4 Moving Average Features Are Important

Recent sales history, especially moving average sales, is one of the strongest predictors of future sales.

### 12.5 Forecasting Supports Inventory Planning

The forecasting output can help the business estimate future demand and reduce the risk of overstocking or stockouts.

---

## 13. Recommendations

### 13.1 Short-Term Recommendations

- Use promotion analysis to identify stores where promotions are most effective.
- Align inventory planning with weekly sales patterns.
- Monitor low-performing stores more frequently.
- Use the dashboard for regular business review.

### 13.2 Medium-Term Recommendations

- Automate the pipeline to run weekly.
- Add product-level or SKU-level data for deeper inventory forecasting.
- Create store-wise alerting for abnormal sales drops.
- Improve forecasting by testing additional models.

### 13.3 Long-Term Recommendations

- Build a production-grade data warehouse.
- Add cloud storage for scalable data handling.
- Include real-time or near-real-time sales data.
- Integrate dashboard outputs with business decision systems.

---

## 14. AI Tools Used

| Tool | How It Was Used |
|---|---|
| ChatGPT | Project explanation, debugging support, report improvement, dashboard guidance |
| GitHub Copilot | Code completion and script development support |
| Claude | Report refinement and documentation review |

All AI-generated suggestions were reviewed, modified, and validated before inclusion in the project.

AI tools were used to support learning and productivity, not to replace student work.

---

## 15. Repository Structure

```text
capstone_retail_project_group_2/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   │   ├── train.csv
│   │   ├── store.csv
│   │   └── test.csv
│   └── processed/
│       ├── rossmann_cleaned.csv
│       ├── rossmann_features.csv
│       └── sales_forecast.csv
├── logs/
├── notebooks/
│   ├── 01_data_inventory.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_schema_and_features.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_dashboard.ipynb
├── pipeline/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── run_pipeline.py
├── reports/
│   ├── FINAL_REPORT.md
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
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 16. How to Reproduce the Project

### Step 1: Clone the Repository

```bash
git clone https://github.com/AnanyaBasu7/capstone_retail_project_group_2.git
cd capstone_retail_project_group_2
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the ETL Pipeline

```bash
python pipeline/run_pipeline.py
```

This generates:

```text
data/processed/rossmann_cleaned.csv
```

### Step 4: Run Notebooks

Open Jupyter Notebook and run the notebooks in order:

```text
01_data_inventory.ipynb
02_data_cleaning.ipynb
03_schema_and_features.ipynb
04_modeling.ipynb
05_dashboard.ipynb
```

### Step 5: Run the Interactive Dashboard Locally

```bash
streamlit run dashboard/app.py
```

### Step 6: Open the Live Dashboard

```text
https://capstone-retail-group2.streamlit.app/
```

---

## 17. Final Deliverables

| Deliverable | Location |
|---|---|
| Code repository | GitHub |
| Raw dataset | `data/raw/` |
| Cleaned dataset | `data/processed/rossmann_cleaned.csv` |
| Feature-engineered dataset | `data/processed/rossmann_features.csv` |
| Forecast output | `data/processed/sales_forecast.csv` |
| Pipeline scripts | `pipeline/` |
| Notebooks | `notebooks/` |
| Reports | `reports/` |
| Interactive dashboard | `dashboard/app.py` |
| Live dashboard | https://capstone-retail-group2.streamlit.app/ |

---

## 18. Conclusion

This project demonstrates a complete beginner-friendly data engineering workflow for retail sales optimization.

The team successfully collected, cleaned, transformed, modeled, and visualized retail sales data. The project produced a reusable ETL pipeline, structured datasets, forecasting results, business insights, and an interactive dashboard.

The final solution can help ABC Retail Corp improve sales analysis, promotion planning, and inventory forecasting.

---

*Team 2 | G25AI1006 · G25AI1007 · G25AI1008 · G25AI1009 · G25AI1010*

*Data Engineering Capstone Project*