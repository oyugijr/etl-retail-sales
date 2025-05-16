import duckdb
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def load_to_duckdb(transformed):
    con = duckdb.connect(config["duckdb"]["path"])
    for name, df in transformed.items():
        con.execute(f"DROP TABLE IF EXISTS {name}")
        con.execute(f"CREATE TABLE {name} AS SELECT * FROM df")
    con.close()
# This function loads the transformed data into DuckDB. It connects to the DuckDB database, drops any existing tables with the same name, and creates new tables with the transformed data.
# The DuckDB connection is closed after loading the data.