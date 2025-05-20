import mysql.connector
import pandas as pd
import yaml
from sqlalchemy import create_engine

# Load configuration
with open("config.yaml") as f:
    config = yaml.safe_load(f)

def extract_data():
    # conn = mysql.connector.connect(**config["mysql"])

     # Use SQLAlchemy to connect to MySQL
    mysql_cfg = config["mysql"]
    connection_url = f"mysql+mysqlconnector://{mysql_cfg['user']}:{mysql_cfg['password']}@{mysql_cfg['host']}/{mysql_cfg['database']}"
    engine = create_engine(connection_url)

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
        """,
        "products": "SELECT * FROM products",
        "productlines": "SELECT * FROM productlines"
    }

    # data = {key: pd.read_sql(q, conn) for key, q in queries.items()}
    # conn.close()
    # return data

    data = {}

    for key, query in queries.items():
        try:
            print(f"Extracting: {key}")
            df = pd.read_sql(query, engine)
            print(f"Loaded {len(df)} records from {key}")
            data[key] = df
        except Exception as e:
            print(f"⚠️ Failed to extract {key}: {e}")

    # conn.close()
    print("✅ Extraction complete. Tables extracted:", list(data.keys()))
    return data

