from etl.transform import clean_sales_data
import pandas as pd

def test_clean_sales_data():
    sales = pd.DataFrame({
        'status': ['completed', 'pending'],
        'quantity': [2, 1],
        'price': [100, 50],
        'product_id': [101, 102],
        'store_id': [1, 2],
        'date': ['2024-01-01', '2024-01-02']
    })
    products = pd.DataFrame({'product_id': [101], 'product_name': ['Laptop']})
    stores = pd.DataFrame({'store_id': [1], 'store_name': ['Nairobi Store']})

    result = clean_sales_data(sales, products, stores)
    assert len(result) == 1
    assert 'total' in result.columns
    assert result['total'].iloc[0] == 200 # 2 * 100 