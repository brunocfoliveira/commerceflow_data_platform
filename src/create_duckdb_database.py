from pathlib import Path
import duckdb


DATABASE_PATH = "data/warehouse/commerceflow.duckdb"
RAW_DATA_PATH = Path("data/raw/olist")


TABLES = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "payments": "olist_order_payments_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}


connection = duckdb.connect(DATABASE_PATH)


for table_name, file_name in TABLES.items():
    file_path = RAW_DATA_PATH / file_name

    print(f"Creating table: {table_name}")

    connection.execute(f"""
        CREATE OR REPLACE TABLE {table_name} AS
        SELECT *
        FROM read_csv_auto('{file_path}')
    """)

print("All tables created successfully.")