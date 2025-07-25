def transform_data(data):
    customers = data["customers"]
    payments = data["payments"]
    orders = data["orders"]
    employees = data["employees"]
    orderdetails = data["orderdetails"]
    products  = data["products"]
    productlines = data["productlines"]

    # Join payments with customers
    payments = payments.merge(customers, on="customerNumber")

    # Calculate total per order
    orders["total"] = orders["quantityOrdered"] * orders["priceEach"]

    return {
        "customers": customers,
        "payments": payments,
        "orders": orders,
        "employees": employees,
        "orderdetails": orderdetails,
        "products": products,
        "productlines": productlines
    }
# This script extracts data from MySQL and transforms it into a format suitable for analysis.