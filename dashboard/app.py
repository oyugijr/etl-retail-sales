import duckdb
import pandas as pd
import streamlit as st

# Set up connection
db_path = "../output/salesDB.duckdb"
con = duckdb.connect(db_path)

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Retail Sales Dashboard")

# Load cleaned data
df = con.execute("SELECT * FROM clean_sales").df()

# Filters
st.sidebar.header("Filter Sales Data")
products = st.sidebar.multiselect("Product", options=df["product_name"].unique(), default=df["product_name"].unique())
stores = st.sidebar.multiselect("Store", options=df["store_name"].unique(), default=df["store_name"].unique())
date_range = st.sidebar.date_input("Date range", [df["date"].min(), df["date"].max()])

# Filter data
filtered = df[
    (df["product_name"].isin(products)) &
    (df["store_name"].isin(stores)) &
    (df["date"] >= pd.to_datetime(date_range[0])) &
    (df["date"] <= pd.to_datetime(date_range[1]))
]

# KPIs
total_sales = filtered["total"].sum()
total_orders = len(filtered)
unique_products = filtered["product_name"].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Unique Products", unique_products)

# Sales Trend
st.subheader("📈 Sales Trend")
sales_by_date = filtered.groupby("date")["total"].sum().reset_index()
st.line_chart(sales_by_date.set_index("date"))

# Sales by Product
st.subheader("📦 Sales by Product")
product_sales = filtered.groupby("product_name")["total"].sum().sort_values(ascending=False)
st.bar_chart(product_sales)

# Sales by Store
st.subheader("🏬 Sales by Store")
store_sales = filtered.groupby("store_name")["total"].sum().sort_values(ascending=False)
st.bar_chart(store_sales)

# Raw data
with st.expander("🔍 View Raw Data"):
    st.dataframe(filtered)

con.close()
