import duckdb

DATABASE_PATH = "data/warehouse/commerceflow.duckdb"

connection = duckdb.connect(DATABASE_PATH)


def get_models_by_prefix(prefix: str):
    query = f"""
    SELECT
        table_name,
        table_type
    FROM information_schema.tables
    WHERE table_schema = 'main'
      AND table_name LIKE '{prefix}%'
    ORDER BY table_name;
    """

    return connection.execute(query).fetchdf()


def preview_table(table_name: str, order_by: str | None = None, limit: int = 10):
    query = f"""
    SELECT *
    FROM {table_name}
    """

    if order_by:
        query += f"\nORDER BY {order_by}"

    query += f"\nLIMIT {limit};"

    return connection.execute(query).fetchdf()


print("DBT staging models:")
staging_models = get_models_by_prefix("stg_")
print(staging_models)


print("\nDBT analytics marts:")
mart_models = get_models_by_prefix("mart_")
print(mart_models)


print("\nPreview of analytics marts:")

mart_preview_config = {
    "mart_sales_by_category": "product_revenue DESC",
    "mart_monthly_revenue": "order_month",
    "mart_state_performance": "product_revenue DESC",
    "mart_customer_retention": None,
    "mart_payment_performance": "total_payment_value DESC",
    "mart_delivery_review_performance": "delivery_status",
    "mart_seller_performance": "product_revenue DESC",
}
for mart_name, order_by in mart_preview_config.items():
    existing_marts = mart_models["table_name"].tolist()

    if mart_name in existing_marts:
        print(f"\nPreview: {mart_name}")
        print(preview_table(mart_name, order_by=order_by, limit=10))
    else:
        print(f"\nSkipping {mart_name}: not found in DuckDB.")