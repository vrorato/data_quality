import pandas as pd
import numpy as np
import pandera.pandas as pa
from pandera import Column, Check
from pandera.errors import SchemaErrors

# =========================
# 1. LOAD DATA
# =========================
customers = pd.read_csv(r"C:\Users\vinicius.cruz\Desktop\3T\ml\Github\Data_Quality\data\raw\customers.csv")
orders = pd.read_csv(r"C:\Users\vinicius.cruz\Desktop\3T\ml\Github\Data_Quality\data\raw\orders.csv")
payments = pd.read_csv(r"C:\Users\vinicius.cruz\Desktop\3T\ml\Github\Data_Quality\data\raw\payments.csv")

# =========================
# 2. SIMULATE DATA QUALITY ISSUES
# =========================

customers.loc[
    customers.sample(frac=0.05, random_state=42).index,
    "customer_zip_code_prefix"
] = np.nan

customers = pd.concat(
    [customers, customers.sample(frac=0.03, random_state=42)],
    ignore_index=True
)

orders.loc[
    orders.sample(frac=0.02, random_state=42).index,
    "order_purchase_timestamp"
] = "2099-01-01"

orders.loc[
    orders.sample(frac=0.01, random_state=42).index,
    "customer_id"
] = "INVALID_CUSTOMER_ID"

# =========================
# 3. DATA TYPE FIXES
# =========================
orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

# =========================
# 4. DATA QUALITY VALIDATION (SAFE MODE)
# =========================

customer_schema = pa.DataFrameSchema({
    "customer_id": Column(str, Check.str_length(32), nullable=False),
    "customer_zip_code_prefix": Column(float, Check.ge(0), nullable=True),
    "customer_city": Column(str),
    "customer_state": Column(str, Check.str_length(2))
})

order_schema = pa.DataFrameSchema({
    "order_id": Column(str, Check.str_length(32)),
    "customer_id": Column(str),
    "order_status": Column(str),
    "order_purchase_timestamp": Column(
        pa.DateTime,
        Check.less_than(pd.Timestamp("today")),
        nullable=True
    )
})

def validate_and_log(df, schema, name):
    try:
        schema.validate(df, lazy=True)
        print(f"✅ {name} passed schema validation.")
    except SchemaErrors as err:
        print(f"⚠️ {name} failed validation.")
        print(err.failure_cases.head(10))

# Validate (non-blocking)
validate_and_log(customers, customer_schema, "Customers")
validate_and_log(orders, order_schema, "Orders")

# =========================
# 5. CLEANING RULES
# =========================

# Remove duplicates
customers = customers.drop_duplicates()

# Remove invalid customers
valid_customers = set(customers["customer_id"])
orders = orders[orders["customer_id"].isin(valid_customers)]

# Fix future or invalid timestamps
orders = orders[
    orders["order_purchase_timestamp"].notna()
]

# Fill missing ZIP codes
customers["customer_zip_code_prefix"] = (
    customers["customer_zip_code_prefix"]
    .fillna(customers["customer_zip_code_prefix"].median())
)

# =========================
# 6. RE-VALIDATE AFTER FIXES
# =========================
validate_and_log(customers, customer_schema, "Customers (Clean)")
validate_and_log(orders, order_schema, "Orders (Clean)")

# =========================
# 7. SAVE CLEAN DATASETS
# =========================
customers.to_csv(r"C:\Users\vinicius.cruz\Desktop\3T\ml\Github\Data_Quality\data\processed\customers_clean.csv", index=False)
orders.to_csv(r"C:\Users\vinicius.cruz\Desktop\3T\ml\Github\Data_Quality\data\processed\orders_clean.csv", index=False)
payments.to_csv(r"C:\Users\vinicius.cruz\Desktop\3T\ml\Github\Data_Quality\data\processed\payments_clean.csv", index=False)

print("🚀 Data Quality Pipeline completed successfully.")

