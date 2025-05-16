import yaml
from etl.extract import extract_sales_data_from_mysql, load_reference_data
from etl.transform import clean_sales_data
from etl.load import load_to_duckdb

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def run_pipeline():
    sales_df = extract_sales_data_from_mysql(config['mysql'])
    products_df = load_reference_data(config['products_path'])
    stores_df = load_reference_data(config['stores_path'])

    clean_df = clean_sales_data(sales_df, products_df, stores_df)
    load_to_duckdb(clean_df, config['db_path'])

if __name__ == "__main__":
    run_pipeline()
# This script orchestrates the ETL process by extracting data from MySQL, transforming it, and loading it into DuckDB.

from extract import extract_data
from transform import transform_data
from load import load_to_duckdb

def run_pipeline():
    raw = extract_data()
    clean = transform_data(raw)
    load_to_duckdb(clean)
    print("✅ ETL pipeline completed.")

if __name__ == "__main__":
    run_pipeline()
