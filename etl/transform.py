import pandas as pd

def clean_sales_data(df, products_df, stores_df):
    df = df[df['status'] == 'completed']
    df['total'] = df['quantity'] * df['price']
    df['date'] = pd.to_datetime(df['date'])
    df = df.merge(products_df, on='product_id', how='left')
    df = df.merge(stores_df, on='store_id', how='left')
    return df


# import pandas as pd

# def clean_sales_data(df):
#     df['date'] = pd.to_datetime(df['date'])
#     df = df.dropna()
#     return df