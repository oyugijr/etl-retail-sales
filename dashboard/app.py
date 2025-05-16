# This is a Streamlit application that provides an interactive dashboard for retail sales data.
# It connects to a DuckDB database, retrieves data based on user-selected filters, and displays key metrics and visualizations.

import streamlit as st
import duckdb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
st.title("📊 Interactive Retail Sales Dashboard")

# DB Connection
con = duckdb.connect("../output/salesDB.duckdb")

# Load unique dates and countries
all_dates = con.execute("SELECT MIN(orderDate), MAX(orderDate) FROM orders").fetchone()
countries = con.execute("SELECT DISTINCT country FROM customers ORDER BY country").df()["country"].tolist()

# Sidebar filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime(all_dates[0]))
end_date = st.sidebar.date_input("End Date", pd.to_datetime(all_dates[1]))
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)

# Format for SQL
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")
country_list = ', '.join(f"'{c}'" for c in selected_countries)

# Key Metrics
st.subheader("🔢 Key Metrics")
query_kpi = f"""
SELECT 
    SUM(total) AS total_sales,
    COUNT(*) AS total_orders
FROM orders o
JOIN customers c ON o.customerNumber = c.customerNumber
WHERE o.orderDate BETWEEN '{start_str}' AND '{end_str}'
AND c.country IN ({country_list})
"""
kpi = con.execute(query_kpi).fetchone()
total_sales, total_orders = kpi
avg_order = round(total_sales / total_orders, 2) if total_orders else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Avg Order Value", f"${avg_order:,.2f}")

# Sales by Product Line
st.subheader("📦 Sales by Product Line")
query1 = f"""
SELECT productLine, SUM(total) AS total_sales
FROM orders o
JOIN customers c ON o.customerNumber = c.customerNumber
WHERE o.orderDate BETWEEN '{start_str}' AND '{end_str}'
AND c.country IN ({country_list})
GROUP BY productLine
ORDER BY total_sales DESC
"""
df1 = con.execute(query1).df()
st.bar_chart(df1.set_index("productLine"))

# Sales by Country
st.subheader("🌍 Sales by Country")
query2 = f"""
SELECT c.country, SUM(p.amount) AS total
FROM payments p
JOIN customers c ON p.customerNumber = c.customerNumber
WHERE c.country IN ({country_list})
GROUP BY c.country
ORDER BY total DESC
"""
df2 = con.execute(query2).df()
fig, ax = plt.subplots()
sns.barplot(x="total", y="country", data=df2, ax=ax)
st.pyplot(fig)

# Top Products
st.subheader("🏆 Top Products")
query3 = f"""
SELECT p.productName, SUM(od.quantityOrdered * od.priceEach) AS revenue
FROM orderdetails od
JOIN products p ON od.productCode = p.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
JOIN customers c ON o.customerNumber = c.customerNumber
WHERE o.orderDate BETWEEN '{start_str}' AND '{end_str}'
AND c.country IN ({country_list})
GROUP BY p.productName
ORDER BY revenue DESC
LIMIT 10
"""
df3 = con.execute(query3).df()
st.dataframe(df3)

# Close connection
con.close()
