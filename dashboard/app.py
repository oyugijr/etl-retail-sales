import streamlit as st
import duckdb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
st.title("📊 Interactive Retail Sales Dashboard")

con = duckdb.connect("salesdb.duckdb")

# --- Sidebar Filters ---
st.sidebar.header("Filters")
all_dates = con.execute("SELECT MIN(orderDate), MAX(orderDate) FROM orders").fetchone()
countries = con.execute("SELECT DISTINCT country FROM customers ORDER BY country").df()["country"].tolist()

default_country = countries[0] if countries else []
start_date = st.sidebar.date_input("Start Date", pd.to_datetime(all_dates[0]))
end_date = st.sidebar.date_input("End Date", pd.to_datetime(all_dates[1]))
selected_countries = st.sidebar.multiselect("Select Countries", countries, default=default_country)

start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")
country_list = ', '.join(f"'{c}'" for c in selected_countries)

# --- Key Metrics ---
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

# --- Sales by Product Line ---
st.subheader("📦 Sales by Product Line")
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

# --- Map Visualization ---
st.subheader("🗺️ Sales by Country (Map)")
map_query = f"""
SELECT c.country, SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM orders o
JOIN orderdetails od ON o.orderNumber = od.orderNumber
JOIN customers c ON o.customerNumber = c.customerNumber
WHERE o.orderDate BETWEEN '{start_str}' AND '{end_str}'
AND c.country IN ({country_list})
GROUP BY c.country
"""
df_map = con.execute(map_query).df()

# Sample coordinates (expand as needed)
country_coords = {
    'USA': (37.0902, -95.7129),
    'Germany': (51.1657, 10.4515),
    'France': (46.6034, 1.8883),
}
df_map["lat"] = df_map["country"].map(lambda c: country_coords.get(c, (0, 0))[0])
df_map["lon"] = df_map["country"].map(lambda c: country_coords.get(c, (0, 0))[1])

layer = pdk.Layer(
    "ScatterplotLayer",
    df_map,
    get_position='[lon, lat]',
    get_radius='total_sales / 100',
    get_fill_color='[200, 30, 0, 160]',
    pickable=True,
)
view_state = pdk.ViewState(latitude=20, longitude=0, zoom=1.2)
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state,
                         tooltip={"text": "{country}\\nSales: ${total_sales}"}))

# --- Monthly Trends ---
st.subheader("📆 Monthly Sales Trends")
monthly_query = f"""
SELECT STRFTIME(o.orderDate, '%Y-%m') AS month, SUM(od.quantityOrdered * od.priceEach) AS total_sales
FROM orders o
JOIN orderdetails od ON o.orderNumber = od.orderNumber
JOIN customers c ON o.customerNumber = c.customerNumber
WHERE o.orderDate BETWEEN '{start_str}' AND '{end_str}'
AND c.country IN ({country_list})
GROUP BY month
ORDER BY month
"""
df_monthly = con.execute(monthly_query).df()
st.line_chart(df_monthly.set_index("month"))

# --- Country Comparison ---
st.subheader("📊 Country Comparison")
compare_query = f"""
SELECT c.country, STRFTIME(o.orderDate, '%Y-%m') AS month, SUM(od.quantityOrdered * od.priceEach) AS sales
FROM orders o
JOIN orderdetails od ON o.orderNumber = od.orderNumber
JOIN customers c ON o.customerNumber = c.customerNumber
WHERE o.orderDate BETWEEN '{start_str}' AND '{end_str}'
AND c.country IN ({country_list})
GROUP BY c.country, month
ORDER BY month
"""
df_compare = con.execute(compare_query).df()
pivot = df_compare.pivot(index="month", columns="country", values="sales").fillna(0)
st.line_chart(pivot)

# --- Download CSV ---
st.subheader("⬇️ Download Data")
csv = df_top.to_csv(index=False).encode('utf-8')
st.download_button("Download Top Products CSV", csv, "top_products.csv", "text/csv")

con.close()
