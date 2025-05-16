# Retail Sales ETL Project

This project extracts sales and payment data from a MySQL database (`salesDB`), processes it using a custom ETL pipeline, and loads it into DuckDB for analytics.

## Features

- Extracts orders, payments, and customer data
- Transforms and cleans using pandas
- Loads into DuckDB
- Streamlit dashboard for visualization
- Jupyter notebook for exploratory analysis

## How to Run

```bash
pip install -r requirements.txt
python etl/pipeline.py
streamlit run dashboard/app.py
jupyter notebook notebooks/Exploratory_Analysis.ipynb
```
