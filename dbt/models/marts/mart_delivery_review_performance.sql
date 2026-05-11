WITH reviews_by_order AS (

    SELECT
        order_id,
        ROUND(AVG(review_score), 2) AS average_review_score
    FROM {{ ref('stg_reviews') }}
    GROUP BY order_id

),

delivered_orders AS (

    SELECT
        order_id,

        DATE_DIFF(
            DATE(order_delivered_customer_date),
            DATE(order_purchase_timestamp),
            DAY
        ) AS delivery_days,

        CASE
            WHEN order_delivered_customer_date <= order_estimated_delivery_date
                THEN 'on_time'
            ELSE 'late'
        END AS delivery_status

    FROM {{ ref('stg_orders') }}

    WHERE order_status = 'delivered'
      AND order_delivered_customer_date IS NOT NULL
      AND order_estimated_delivery_date IS NOT NULL

)

SELECT
    d.delivery_status,
    COUNT(DISTINCT d.order_id) AS delivered_orders,
    ROUND(AVG(d.delivery_days), 2) AS average_delivery_days,
    ROUND(AVG(r.average_review_score), 2) AS average_review_score

FROM delivered_orders AS d

LEFT JOIN reviews_by_order AS r
    ON d.order_id = r.order_id

GROUP BY d.delivery_status