#!/bin/bash

set -e

echo "Starting CommerceFlow local pipeline..."

echo "1. Loading raw CSV files into DuckDB..."
python src/create_duckdb_database.py

echo "2. Running dbt models..."
dbt run --project-dir dbt --profiles-dir .

echo "3. Running dbt tests..."
dbt test --project-dir dbt --profiles-dir .

echo "4. Checking final marts..."
python src/check_marts.py

echo "CommerceFlow pipeline completed successfully."