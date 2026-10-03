import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px


DB_PATH = "pharmeasy.db"


st.set_page_config(
    page_title="PharmEasy Regional Pulse",
    layout="wide"
)


@st.cache_data
def load_data():

    conn = sqlite3.connect(DB_PATH)

    orders = pd.read_sql_query(
        """
        SELECT *
        FROM orders_clean
        """,
        conn
    )

    regions = pd.read_sql_query(
        """
        SELECT *
        FROM regions_master
        """,
        conn
    )

    conn.close()

    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["month"] = orders["order_date"].dt.strftime("%Y-%m")

    return orders, regions


orders, regions = load_data()


st.title("PharmEasy Regional Pulse")

st.write(
    "Regional sales performance dashboard for April, May and June 2026."
)


# ---------------------------------------------------------
# REGION FILTER
# ---------------------------------------------------------

region_options = ["All Regions"] + sorted(
    orders["region"].dropna().unique().tolist()
)

selected_region = st.selectbox(
    "Select Region",
    region_options
)


if selected_region == "All Regions":
    filtered_orders = orders.copy()
else:
    filtered_orders = orders[
        orders["region"] == selected_region
    ].copy()


# ---------------------------------------------------------
# KPI CALCULATIONS
# ---------------------------------------------------------

total_sales = filtered_orders["sales_inr"].sum()

total_profit = filtered_orders["profit_inr"].sum()

total_orders = filtered_orders["order_id"].nunique()


# ---------------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------------

st.subheader("Executive Summary")

st.write(
    f"Total sales are INR {total_sales:,.2f} from "
    f"{total_orders:,} distinct orders. "
    f"Total profit is INR {total_profit:,.2f}. "
    f"The dashboard shows monthly sales movements across the selected region. "
    f"Use the category and regional charts below to understand where the "
    f"sales movement comes from and review flagged changes before taking action."
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Sales (INR)",
        f"₹{total_sales:,.2f}"
    )

with col2:
    st.metric(
        "Total Profit (INR)",
        f"₹{total_profit:,.2f}"
    )

with col3:
    st.metric(
        "Distinct Orders",
        f"{total_orders:,}"
    )


# ---------------------------------------------------------
# CATEGORY LEVEL
# ---------------------------------------------------------

st.header("Category Level")

category_sales = (
    filtered_orders
    .groupby("category", as_index=False)["sales_inr"]
    .sum()
    .sort_values("sales_inr", ascending=False)
)


col1, col2 = st.columns(2)


with col1:

    st.subheader("Which categories generate sales?")

    fig_category = px.pie(
        category_sales,
        names="category",
        values="sales_inr",
        title="Which categories generate sales?"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


with col2:

    st.subheader("Sales by Category")

    st.dataframe(
        category_sales,
        use_container_width=True
    )


# ---------------------------------------------------------
# REGION LEVEL
# ---------------------------------------------------------

st.header("Region Level")


region_sales = (
    filtered_orders
    .groupby("region", as_index=False)["sales_inr"]
    .sum()
    .sort_values("sales_inr", ascending=False)
)


st.subheader("Which regions generate the most sales?")


fig_region = px.bar(
    region_sales,
    x="region",
    y="sales_inr",
    title="Which regions generate the most sales?",
    labels={
        "region": "Region",
        "sales_inr": "Sales (INR)"
    }
)

fig_region.update_yaxes(rangemode="tozero")


st.plotly_chart(
    fig_region,
    use_container_width=True
)


# ---------------------------------------------------------
# MONTHLY TREND
# ---------------------------------------------------------

st.subheader("How do sales change by month?")


monthly_sales = (
    filtered_orders
    .groupby(["month", "region"], as_index=False)["sales_inr"]
    .sum()
)


fig_trend = px.line(
    monthly_sales,
    x="month",
    y="sales_inr",
    color="region",
    markers=True,
    title="How do sales change by month?",
    labels={
        "month": "Month",
        "sales_inr": "Sales (INR)",
        "region": "Region"
    }
)

fig_trend.update_yaxes(rangemode="tozero")


st.plotly_chart(
    fig_trend,
    use_container_width=True
)


# ---------------------------------------------------------
# DETAIL LEVEL
# ---------------------------------------------------------

st.header("Detail Level")

detail = (
    filtered_orders
    .groupby(
        ["region", "month"],
        as_index=False
    )
    .agg(
        orders=("order_id", "nunique"),
        sales_inr=("sales_inr", "sum"),
        profit_inr=("profit_inr", "sum")
    )
)


detail = detail.sort_values(
    ["region", "month"]
)


st.subheader("Region × Month Performance")

st.dataframe(
    detail,
    use_container_width=True
)


# ---------------------------------------------------------
# FLAGGED REGIONS
# ---------------------------------------------------------

st.header("Review Flags")

st.write(
    "Regions with large month-on-month movement should be reviewed "
    "before operational action is taken."
)


changes = (
    monthly_sales
    .pivot(
        index="region",
        columns="month",
        values="sales_inr"
    )
)


if "2026-04" in changes.columns and "2026-05" in changes.columns:

    changes["Apr-May %"] = (
        (changes["2026-05"] - changes["2026-04"])
        / changes["2026-04"]
        * 100
    )

else:

    changes["Apr-May %"] = 0


if "2026-05" in changes.columns and "2026-06" in changes.columns:

    changes["May-Jun %"] = (
        (changes["2026-06"] - changes["2026-05"])
        / changes["2026-05"]
        * 100
    )

else:

    changes["May-Jun %"] = 0


changes["Flagged"] = (
    (changes["Apr-May %"].abs() > 8)
    |
    (changes["May-Jun %"].abs() > 8)
)


flagged = changes[changes["Flagged"]].reset_index()


st.dataframe(
    flagged[
        [
            "region",
            "Apr-May %",
            "May-Jun %",
            "Flagged"
        ]
    ],
    use_container_width=True
)


st.caption(
    "An 8% movement is an operational review threshold, "
    "not proof of a statistically significant change."
)