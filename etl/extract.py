import pandas as pd
import mysql.connector
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def extract_sales_data():
    conn = mysql.connector.connect(**config['mysql'])
    query = f"""
        SELECT s.date, s.product_id, p.product_name, s.store_id, st.store_name, s.quantity, s.price, s.quantity * s.price AS total
        FROM {config['tables']['sales']} s
        JOIN {config['tables']['products']} p ON s.product_id = p.product_id
        JOIN {config['tables']['stores']} st ON s.store_id = st.store_id
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# def extract_sales_data_from_mysql(config: dict) -> pd.DataFrame:
#     conn = mysql.connector.connect(**config)
#     query = """
#         SELECT sale_id, product_id, store_id, quantity, price, status, date
#         FROM sales
#     """
#     df = pd.read_sql(query, conn)
#     conn.close()
#     return df

# def load_reference_data(path: str) -> pd.DataFrame:
#     return pd.read_csv(path)
