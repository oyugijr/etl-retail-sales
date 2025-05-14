# Technical Documentation

## Overview

This ETL pipeline processes retail sales data by:

- Extracting data from a MySQL database
- Transforming the data to ensure quality and consistency
- Loading the transformed data into a DuckDB database

## Components

### Extraction

- Connects to the MySQL database using credentials specified in `config.yaml`.
- Retrieves sales data from the `sales` table.

### Transformation

- Filters out incomplete transactions.
- Calculates the total amount for each transaction.
- Converts date strings to datetime objects.
- Merges sales data with product and store reference data.

### Loading

- Writes the transformed data into a DuckDB database located at the path specified in `config.yaml`.

## Configuration

All configurations are managed through the `config.yaml` file, including:

- MySQL connection details
- Paths to reference data files
- Output path for the DuckDB database

## Testing

Unit tests are provided in the `tests/` directory to validate the transformation logic.

## Dependencies

- pandas
- duckdb
- mysql-connector-python
- pyyaml
