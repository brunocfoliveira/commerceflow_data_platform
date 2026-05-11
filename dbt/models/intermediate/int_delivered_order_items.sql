SELECT
    oi.order_id,
    oi.order_item_id,
    oi.product_id,
    oi.seller_id,

    o.customer_id,
    c.customer_unique_id,
    c.customer_state,

    o.order_purchase_timestamp,
    DATE_TRUNC(DATE(o.order_purchase_timestamp), MONTH) AS order_month,

    COALESCE(
        ct.product_category_name_english,
        p.product_category_name,
        'unknown'
    ) AS category,

    oi.price,
    oi.freight_value

FROM {{ ref('stg_order_items') }} AS oi

JOIN {{ ref('stg_orders') }} AS o
    ON oi.order_id = o.order_id

JOIN {{ ref('stg_customers') }} AS c
    ON o.customer_id = c.customer_id

LEFT JOIN {{ ref('stg_products') }} AS p
    ON oi.product_id = p.product_id

LEFT JOIN {{ ref('stg_category_translation') }} AS ct
    ON p.product_category_name = ct.product_category_name

WHERE o.order_status = 'delivered'