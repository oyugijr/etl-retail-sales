import mysql.connector
import pandas as pd
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def extract_data():
    conn = mysql.connector.connect(**config["mysql"])

    queries = {
        "customers": "SELECT * FROM customers",
        "payments": "SELECT * FROM payments",
        "orders": """
            SELECT o.orderNumber, o.orderDate, o.customerNumber,
                   od.productCode, od.quantityOrdered, od.priceEach,
                   p.productName, p.productLine
            FROM orders o
            JOIN orderdetails od ON o.orderNumber = od.orderNumber
            JOIN products p ON p.productCode = od.productCode
        """,
        "employees": """
            SELECT e.employeeNumber, e.firstName, e.lastName, o.city, o.country
            FROM employees e
            JOIN offices o ON e.officeCode = o.officeCode
        """
    }

    data = {key: pd.read_sql(q, conn) for key, q in queries.items()}
    conn.close()
    return data

# def load_reference_data():
#     with open("config.yaml") as f:
#         config = yaml.safe_load(f)
#     products_df = pd.read_csv(config["products_path"])
#     stores_df = pd.read_csv(config["stores_path"])
#     return products_df, stores_df

# def extract_sales_data_from_mysql(mysql_config):
#     conn = mysql.connector.connect(**mysql_config)
#     sales_df = pd.read_sql("SELECT * FROM sales", conn)
#     conn.close()
#     return sales_df

# def load_to_duckdb(data, db_path):
#     import duckdb
#     con = duckdb.connect(db_path)
#     for name, df in data.items():
#         con.execute(f"DROP TABLE IF EXISTS {name}")
#         con.execute(f"CREATE TABLE {name} AS SELECT * FROM df")
#     con.close()
    