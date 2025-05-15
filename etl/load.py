# import duckdb

# def load_to_duckdb(df, db_path: str, table_name: str = 'clean_sales'):
#     con = duckdb.connect(db_path)
#     con.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM df")
#     con.close()


import duckdb
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def load_to_duckdb(df):
    con = duckdb.connect(config['duckdb']['path'])
    con.execute("DROP TABLE IF EXISTS clean_sales")
    con.execute("CREATE TABLE clean_sales AS SELECT * FROM df")
    con.close()
