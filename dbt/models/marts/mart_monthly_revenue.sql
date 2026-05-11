SELECT
    order_month,

    COUNT(DISTINCT order_id) AS delivered_orders,
    COUNT(*) AS items_sold,

    ROUND(SUM(price), 2) AS product_revenue,
    ROUND(SUM(freight_value), 2) AS freight_revenue,

    ROUND(
        SUM(price) / COUNT(DISTINCT order_id),
        2
    ) AS average_order_value

FROM {{ ref('int_delivered_order_items') }}

GROUP BY order_month