from pathlib import Path
import duckdb

DATABASE_PATH = "data/warehouse/commerceflow.duckdb"
ORDERS_CSV = "data/raw/olist/olist_orders_dataset.csv"

connection = duckdb.connect(DATABASE_PATH)

connection.execute(f"""
CREATE OR REPLACE TABLE orders AS
SELECT *
FROM read_csv_auto('{ORDERS_CSV}')
""")

print("Orders table created successfully.")

result = connection.execute("SELECT * FROM orders LIMIT 5").fetchdf()
print(result)