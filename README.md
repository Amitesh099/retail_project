# Retail Sales Optimization — ABC Retail Corp

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://capstone-retail-group2.streamlit.app/)

## Overview

This repository contains the Data Engineering capstone project for ABC Retail Corp.

The project uses the Rossmann Store Sales dataset to build an end-to-end retail sales optimization workflow. The main goal is to clean raw retail data, build an ETL pipeline, create analytical features, train a sales forecasting model, and present insights using reports and an interactive dashboard.

---

## Business Objective

ABC Retail Corp wants to improve:

- Sales trend analysis
- Promotion planning
- Store-level performance monitoring
- Inventory planning
- Sales forecasting
- Business reporting through dashboards

This project converts raw retail sales data into meaningful business insights.

---

## Dataset

Dataset used:

```text
Rossmann Store Sales Dataset
```

Main files used:

| File | Purpose |
|---|---|
| `train.csv` | Historical daily sales data |
| `store.csv` | Store-level information |
| `test.csv` | Test/reference dataset |

Dataset location in this repo:

```text
data/raw/
```

---

## Project Workflow

```text
Raw CSV files
→ Data quality check
→ Data cleaning
→ ETL pipeline
→ Cleaned dataset
→ Feature engineering
→ Sales forecasting model
→ Static visualizations
→ Interactive Streamlit dashboard
→ Final report and recommendations
```

---

## Repository Structure

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
│       └── rossmann_cleaned.csv
├── logs/
├── notebooks/
├── pipeline/
│   ├── __init__.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── run_pipeline.py
├── reports/
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Technology Stack

| Area | Tools Used |
|---|---|
| Programming | Python |
| Data processing | Pandas, NumPy |
| Modeling | Scikit-learn |
| Visualization | Matplotlib, Seaborn, Plotly |
| Dashboard | Streamlit |
| Documentation | Markdown |
| Version control | Git and GitHub |

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/AnanyaBasu7/capstone_retail_project_group_2.git
cd capstone_retail_project_group_2
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## How to Run the ETL Pipeline

Run this command from the project root:

```bash
python pipeline/run_pipeline.py
```

This reads the raw files from:

```text
data/raw/
```

and creates the cleaned dataset:

```text
data/processed/rossmann_cleaned.csv
```

---

## How to Run the Notebooks

Open Jupyter Notebook or VS Code and run the notebooks in sequence.

Suggested order:

```text
01_data_inventory.ipynb
02_data_cleaning.ipynb
03_schema_and_features.ipynb
04_modeling.ipynb
05_dashboard.ipynb
```

The notebooks cover data inventory, cleaning, schema design, feature engineering, modeling, and visualization.

---

## How to Run the Interactive Dashboard Locally

Run:

```bash
streamlit run dashboard/app.py
```

The dashboard will open in the browser.

Dashboard features:

- Date range filter
- Store filter
- Promotion filter
- KPI cards
- Daily sales trend
- Top 10 stores by sales
- Promotion impact chart
- Monthly sales trend
- Forecast output section

---

## Live Dashboard

The project includes a live interactive dashboard deployed using Streamlit Community Cloud.

Live dashboard link:

```text
https://capstone-retail-group2.streamlit.app/
```

---

## Project Outputs

| Output | Location | Purpose |
|---|---|---|
| Cleaned dataset | `data/processed/rossmann_cleaned.csv` | Cleaned and merged sales data |
| Feature engineering | `notebooks/` | Feature generation and transformation steps |
| Forecasting output | Generated from modeling notebook | Actual vs predicted sales output |
| Pipeline scripts | `pipeline/` | Automated ETL workflow |
| Reports | `reports/` | Weekly and final documentation |
| Dashboard app | `dashboard/app.py` | Interactive dashboard |
| Live dashboard | https://capstone-retail-group2.streamlit.app/ | Public deployed dashboard |

---

## Model Summary

The project uses a Random Forest Regressor to forecast sales.

| Metric | Value |
|---|---|
| Model | Random Forest Regressor |
| MAE | 718.74 |
| RMSE | 1068.83 |
| RMSPE | 13.16% |

---

## Key Insights

- Promotions have a strong impact on sales.
- Sales patterns vary by day of the week.
- Store-level performance differs across the network.
- Moving average sales features are important for forecasting.
- Forecasting can help improve inventory planning.
- Interactive dashboards make business insights easier to understand.

---

## Evidence Screenshots

Important execution and dashboard screenshots are stored in:

```text
reports/screenshots/
```

Recommended screenshots:

- Pipeline execution success
- Streamlit dashboard homepage
- Dashboard filters applied
- Forecast section, if available
- Public live dashboard page

---

## AI Tools Used

| Tool | Usage |
|---|---|
| ChatGPT | Explanation, debugging, dashboard guidance, documentation support |
| GitHub Copilot | Code completion support |
| Claude | Report refinement and review |

All AI-generated suggestions were reviewed and validated before inclusion.

---

## Team

Team 2

| Student ID | Name |
|---|---|
| G25AI1006 | Amandeep |
| G25AI1007 | Amitesh Srivastava |
| G25AI1008 | Ananya Basu |
| G25AI1009 | Anbu Karthika Durairaj |
| G25AI1010 | Aniket |

---

## Final Deliverables

| Deliverable | Status |
|---|---|
| GitHub repository | Completed |
| Raw dataset | Completed |
| Cleaned dataset | Completed |
| ETL pipeline | Completed |
| Feature engineering | Completed |
| Forecasting model | Completed |
| Static visualizations | Completed |
| Interactive dashboard | Completed |
| Live dashboard deployment | Completed |
| Final report | Completed |
| Presentation | Completed |

---

## Conclusion

This project demonstrates a complete data engineering workflow for retail sales optimization.

It starts with raw CSV files and ends with cleaned datasets, pipeline scripts, forecasting output, visual insights, and an interactive dashboard.

The final solution can help ABC Retail Corp make better decisions around sales forecasting, promotion planning, and inventory management.