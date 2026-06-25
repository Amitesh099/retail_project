# Week 4 Report — Schema Design and Feature Engineering

## Data warehouse design (star schema)

fact_sales (central table)
  ├── dim_date    (joined on Date)
  ├── dim_store   (joined on Store)
  └── dim_promo   (joined on Promo + StateHoliday + SchoolHoliday)

Stored as: data/processed/rossmann_warehouse.db (SQLite)

## Optimization strategies
- Index on fact_sales(Store): speeds up store-level aggregation queries
- Index on fact_sales(Date): speeds up time-series and range queries
- Index on fact_sales(Promo): speeds up promotion analysis queries

## Feature engineering summary
| Feature | Type | Rationale |
|---------|------|-----------|
| Year, Month, Week, Quarter | Time | Capture seasonal patterns |
| IsWeekend | Time | Weekend shopping behavior |
| Sales_Lag7/14/30 | Lag | Recent sales history for forecasting |
| Sales_MA7/30 | Rolling avg | Smooth short/long term trends |
| Store_AvgSales | Aggregate | Store baseline performance |
| StoreType_enc | Encoded | ML-ready categorical |
| HasCompetition | Binary | Competitive pressure flag |
| CompetitionDistance_log | Transform | Log reduces skew in large distances |
| Promo_Weekend | Interaction | Promo effect amplified on weekends |

## Output files
- rossmann_warehouse.db — star schema SQLite database
- rossmann_features.csv — fully engineered dataset (X cols) ready for modeling

## AI tools used
- claude