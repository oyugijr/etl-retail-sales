import pandas as pd
from etl.transform import transform_data

def test_transform_data():
    raw = {
        "customers": pd.DataFrame({"customerNumber": [1], "customerName": ["ABC"]}),
        "payments": pd.DataFrame({"customerNumber": [1], "amount": [100.0]}),
        "orders": pd.DataFrame({
            "orderNumber": [10100],
            "quantityOrdered": [10],
            "priceEach": [20.0],
            "productCode": ["S10_1678"],
            "productName": ["Model Car"],
            "productLine": ["Classic Cars"]
        }),
        "employees": pd.DataFrame({"employeeNumber": [1002], "firstName": ["John"], "lastName": ["Doe"]})
    }

    result = transform_data(raw)
    assert "total" in result["orders"].columns
