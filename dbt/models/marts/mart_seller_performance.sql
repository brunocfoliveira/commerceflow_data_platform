SELECT
    s.seller_id,
    s.seller_city,
    s.seller_state,

    COUNT(DISTINCT i.order_id) AS delivered_orders,
    COUNT(*) AS items_sold,

    ROUND(SUM(i.price), 2) AS product_revenue,
    ROUND(SUM(i.freight_value), 2) AS freight_revenue,

    ROUND(
        SUM(i.price) / COUNT(DISTINCT i.order_id),
        2
    ) AS average_order_value

FROM {{ ref('int_delivered_order_items') }} AS i

JOIN {{ ref('stg_sellers') }} AS s
    ON i.seller_id = s.seller_id

GROUP BY
    s.seller_id,
    s.seller_city,
    s.seller_state