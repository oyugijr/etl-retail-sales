import streamlit as st
import duckdb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Page config
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
st.title("📊 Interactive Retail Sales Dashboard")

# Connect to DuckDB
con = duckdb.connect("output/salesDB.duckdb")

# --- Sidebar Filters ---
st.sidebar.header("Filters")

# Load filter values
all_dates = con.execute("SELECT MIN(orderDate), MAX(orderDate) FROM orders").fetchone()
countries = con.execute("SELECT DISTINCT country FROM customers ORDER BY country").df()["country"].tolist()

start_date = st.sidebar.date_input("Start Date", pd.to_datetime(all_dates[0]))
end_date = st.sidebar.date_input("End Date", pd.to_datetime(all_dates[1]))
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=countries)

# Format values for query
start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")
country_list = ', '.join(f"'{c}'" for c in selected_countries)

# --- Key Metrics ---
st.subheader("🔢 Key Metrics")

# query_kpi = f"""
# SELECT 
#     SUM(total) AS total_sales,
#     COUNT(*) AS total_orders
# FROM orders o
# JOIN customers c ON o.customerNumber = c.customerNumber
# WHERE o.orderDate BETWEEN '{start_str}' AND '{end_str}'
# AND c.country IN ({country_list})
# """

query_kpi = f"""
SELECT 
    SUM(od.quantityOrdered * od.priceEach) AS total_sales,
    COUNT(DISTINCT o.orderNumber) AS total_orders
FROM orders o
JOIN customers c ON o.customerNumber = c.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
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

# --- Sales by Product Line ---
st.subheader("📦 Sales by Product Line")

# query_product_line = f"""
# SELECT productLine, SUM(total) AS total_sales
# FROM orders o
# JOIN customers c ON o.customerNumber = c.customerNumber
# JOIN orderdetails od ON o.orderNumber = od.orderNumber
# JOIN products p ON od.productCode = p.productCode
# WHERE o.orderDate BETWEEN '{start_str}' AND '{end_str}'
# AND c.country IN ({country_list})
# GROUP BY productLine
# ORDER BY total_sales DESC
# """

query_product_line = f"""
SELECT p.productLine, SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM orders o
JOIN customers c ON o.customerNumber = c.customerNumber
JOIN orderdetails od ON o.orderNumber = od.orderNumber
JOIN products p ON od.productCode = p.productCode
WHERE o.orderDate BETWEEN '{start_str}' AND '{end_str}'
AND c.country IN ({country_list})
GROUP BY p.productLine
ORDER BY total_sales DESC
"""
# Execute query and convert to DataFrame
df_product = con.execute(query_product_line).df()
st.bar_chart(df_product.set_index("productLine"))

# --- Sales by Country ---
st.subheader("🌍 Sales by Country")

query_country = f"""
SELECT c.country, SUM(p.amount) AS total
FROM payments p
JOIN customers c ON p.customerNumber = c.customerNumber
WHERE c.country IN ({country_list})
GROUP BY c.country
ORDER BY total DESC
"""
df_country = con.execute(query_country).df()

fig, ax = plt.subplots()
sns.barplot(x="total", y="country", data=df_country, ax=ax)
st.pyplot(fig)

# --- Top Products ---
st.subheader("🏆 Top Products")

query_top_products = f"""
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
df_top = con.execute(query_top_products).df()
st.dataframe(df_top)

# Close DB connection
con.close()
