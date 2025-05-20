import mysql.connector
import pandas as pd
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def extract_data():
    conn = mysql.connector.connect(**config["mysql"])

    queries = {
        "customers": "SELECT * FROM customers",
        "orderdetails": "SELECT * FROM orderdetails",
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

    