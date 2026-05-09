# How many orders exist by status?
from time import time

import duckdb

DATABASE_PATH = "data/warehouse/commerceflow.duckdb"

connection = duckdb.connect(DATABASE_PATH)

query = """ SELECT order_status, COUNT(*) AS total_orders
                            FROM orders
                            GROUP BY order_status
                            ORDER BY total_orders DESC;"""

result = connection.execute(query).fetchdf()

print(result)

#How many sells?
query = """ SELECT ROUND(SUM(oi.price), 2) AS product_revenue,
                   ROUND(SUM(oi.freight_value),2) AS freight_revenue,
                   COUNT (DISTINCT o.order_id) AS delivered_orders,
                   COUNT(*) AS total_order_items
            FROM order_items AS oi
            JOIN orders AS o
               ON oi.order_id = o.order_id
            WHERE o.order_status = 'delivered';"""

result = connection.execute(query).fetchdf()

print(result)

#Which category has the most sells?

import duckdb

DATABASE_PATH = "data/warehouse/commerceflow.duckdb"

connection = duckdb.connect(DATABASE_PATH)

query = """
SELECT
    COALESCE(ct.product_category_name_english, p.product_category_name, 'unknown') AS category,
    ROUND(SUM(oi.price), 2) AS revenue,
    COUNT(DISTINCT o.order_id) AS orders,
    COUNT(*) AS items_sold
FROM order_items AS oi
JOIN orders AS o
    ON oi.order_id = o.order_id
LEFT JOIN products AS p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation AS ct
    ON p.product_category_name = ct.product_category_name
WHERE o.order_status = 'delivered'
GROUP BY category
ORDER BY revenue DESC
LIMIT 10;
"""

result = connection.execute(query).fetchdf()

print(result)

# What is the average value of each order?
query = """
SELECT
    ROUND(SUM(oi.price), 2) AS product_revenue,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS average_order_value 
FROM order_items AS oi
JOIN orders AS o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered';
"""

result = connection.execute(query).fetchdf()
print(result)

#How has the recipe evolved over time?
query = """
SELECT
    DATE_TRUNC('month', CAST(o.order_purchase_timestamp AS TIMESTAMP)) AS order_month,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    ROUND(SUM(oi.price), 2) AS product_revenue,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM order_items AS oi
JOIN orders AS o
    ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY order_month
ORDER BY order_month;
"""

result = connection.execute(query).fetchdf()
print(result)

#Which customers come back to buy again?
query = """
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) AS total_orders
    FROM orders AS o
    JOIN customers AS c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)

SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(
        SUM(CASE WHEN total_orders > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS repeat_customer_percentage
FROM customer_orders;
"""

result = connection.execute(query).fetchdf()
print(result)

#Locations with best performance
query = """
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS delivered_orders,
    ROUND(SUM(oi.price), 2) AS product_revenue,
    ROUND(SUM(oi.price) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM order_items AS oi
JOIN orders AS o
    ON oi.order_id = o.order_id
JOIN customers AS c
    ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY product_revenue DESC
LIMIT 10;
"""

result = connection.execute(query).fetchdf()
print(result)