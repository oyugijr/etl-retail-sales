def transform_data(data):
    customers = data["customers"]
    payments = data["payments"]
    orders = data["orders"]
    employees = data["employees"]

    # Join payments with customers
    payments = payments.merge(customers, on="customerNumber")

    # Calculate total per order
    orders["total"] = orders["quantityOrdered"] * orders["priceEach"]

    return {
        "payments": payments,
        "orders": orders,
        "employees": employees
    }
# This script extracts data from MySQL and transforms it into a format suitable for analysis.