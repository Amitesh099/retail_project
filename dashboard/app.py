from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Retail Sales Optimization Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Retail Sales Optimization Dashboard")
st.markdown(
    "Interactive dashboard for ABC Retail Corp using the Rossmann Store Sales dataset."
)

# -------------------------------------------------------------------
# Data path
# -------------------------------------------------------------------
DATA_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "processed"
    / "rossmann_cleaned.csv"
)


# -------------------------------------------------------------------
# Load data
# -------------------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


if not DATA_PATH.exists():
    st.error(
        "The cleaned dataset was not found. Please run `python pipeline/run_pipeline.py` first."
    )
    st.stop()


df = load_data()

required_columns = ["Date", "Store", "Sales"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"Missing required columns in dataset: {missing_columns}")
    st.stop()


# -------------------------------------------------------------------
# Sidebar filters
# -------------------------------------------------------------------
st.sidebar.header("Filters")

min_date = df["Date"].min()
max_date = df["Date"].max()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

store_list = sorted(df["Store"].dropna().unique())

selected_stores = st.sidebar.multiselect(
    "Select stores",
    options=store_list,
    default=store_list[:10],
)

filtered_df = df.copy()

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["Date"] >= pd.to_datetime(start_date))
        & (filtered_df["Date"] <= pd.to_datetime(end_date))
    ]

if selected_stores:
    filtered_df = filtered_df[filtered_df["Store"].isin(selected_stores)]

if "Promo" in filtered_df.columns:
    promo_filter = st.sidebar.selectbox(
        "Promotion filter",
        options=["All", "Promo Only", "No Promo"],
    )

    if promo_filter == "Promo Only":
        filtered_df = filtered_df[filtered_df["Promo"] == 1]
    elif promo_filter == "No Promo":
        filtered_df = filtered_df[filtered_df["Promo"] == 0]


# -------------------------------------------------------------------
# KPI cards
# -------------------------------------------------------------------
total_sales = filtered_df["Sales"].sum()
average_sales = filtered_df["Sales"].mean()
total_stores = filtered_df["Store"].nunique()
total_records = len(filtered_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Average Sales", f"{average_sales:,.0f}")
col3.metric("Stores", f"{total_stores:,}")
col4.metric("Records", f"{total_records:,}")

st.divider()


# -------------------------------------------------------------------
# Sales trend
# -------------------------------------------------------------------
st.subheader("Sales Trend Over Time")

daily_sales = (
    filtered_df.groupby("Date", as_index=False)["Sales"]
    .sum()
    .sort_values("Date")
)

fig_daily = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Daily Sales Trend",
)

st.plotly_chart(fig_daily, use_container_width=True)


# -------------------------------------------------------------------
# Top stores and promotion impact
# -------------------------------------------------------------------
col5, col6 = st.columns(2)

with col5:
    st.subheader("Top 10 Stores by Sales")

    top_stores = (
        filtered_df.groupby("Store", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    fig_top_stores = px.bar(
        top_stores,
        x="Store",
        y="Sales",
        title="Top Performing Stores",
    )

    st.plotly_chart(fig_top_stores, use_container_width=True)


with col6:
    st.subheader("Promotion Impact")

    if "Promo" in filtered_df.columns:
        promo_sales = (
            filtered_df.groupby("Promo", as_index=False)["Sales"]
            .mean()
        )

        promo_sales["Promo"] = promo_sales["Promo"].map(
            {
                0: "No Promo",
                1: "Promo",
            }
        )

        fig_promo = px.bar(
            promo_sales,
            x="Promo",
            y="Sales",
            title="Average Sales: Promo vs No Promo",
        )

        st.plotly_chart(fig_promo, use_container_width=True)
    else:
        st.info("Promo column not available.")


# -------------------------------------------------------------------
# Monthly trend
# -------------------------------------------------------------------
st.subheader("Monthly Sales Trend")

filtered_df = filtered_df.copy()
filtered_df["Year"] = filtered_df["Date"].dt.year
filtered_df["Month"] = filtered_df["Date"].dt.month

monthly_sales = (
    filtered_df.groupby(["Year", "Month"], as_index=False)["Sales"]
    .sum()
)

monthly_sales["Year_Month"] = (
    monthly_sales["Year"].astype(str)
    + "-"
    + monthly_sales["Month"].astype(str).str.zfill(2)
)

fig_monthly = px.line(
    monthly_sales,
    x="Year_Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend",
)

st.plotly_chart(fig_monthly, use_container_width=True)


# -------------------------------------------------------------------
# Forecasting model summary
# -------------------------------------------------------------------
st.subheader("Forecasting Model Summary")

col7, col8, col9 = st.columns(3)

col7.metric("MAE", "718.74")
col8.metric("RMSE", "1068.83")
col9.metric("RMSPE", "13.16%")

st.markdown(
    """
The sales forecasting model was built using a **Random Forest Regressor**.

The model uses historical sales patterns, promotion information, date-based features,
moving averages, lag features, and store-level attributes to predict store-level sales.

The forecast output supports:

- Inventory planning
- Promotion analysis
- Store performance monitoring
- Sales trend understanding
"""
)


# -------------------------------------------------------------------
# Business insights
# -------------------------------------------------------------------
st.subheader("Business Insights")

st.markdown(
    """
- Promotion days can be compared against non-promotion days to understand campaign impact.
- Store-wise sales ranking helps identify high-performing and low-performing stores.
- Monthly trends help detect seasonal demand patterns.
- Forecasting supports better inventory planning and business decision-making.
- The dashboard allows users to filter stores and dates without manually checking raw CSV files.
"""
)