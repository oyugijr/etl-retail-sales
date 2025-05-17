import duckdb
import yaml
import pandas as pd

with open("config.yaml") as file:
    config = yaml.safe_load(file)

print(config)

def load_to_duckdb(dfs, dict):
    # Connect to DuckDB file
    con = duckdb.connect(config["duckdb"]["path"])

    # Iterate and register each DataFrame
    for name, df in dfs.items():
        con.register(name, df)
        con.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM {name}")
        print(f"Loaded table: {name}")

    con.close()


# def load_to_duckdb(transformed):
#     con = duckdb.connect(config["duckdb"]["path"])
#     for name, df in transformed.items():
#         con.execute(f"DROP TABLE IF EXISTS {name}")
#         con.execute(f"CREATE TABLE {name} AS SELECT * FROM df")
#     con.close()
# This function loads the transformed data into DuckDB. It connects to the DuckDB database, drops any existing tables with the same name, and creates new tables with the transformed data.
# The DuckDB connection is closed after loading the data.



# def load_to_duckdb(dfs: dict):