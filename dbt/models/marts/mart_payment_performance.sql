SELECT
    p.payment_type,

    COUNT(DISTINCT p.order_id) AS orders,
    COUNT(*) AS payment_records,

    ROUND(SUM(p.payment_value), 2) AS total_payment_value,
    ROUND(AVG(p.payment_value), 2) AS average_payment_value,

    ROUND(AVG(p.payment_installments), 2) AS average_installments

FROM {{ ref('stg_payments') }} AS p

JOIN {{ ref('stg_orders') }} AS o
    ON p.order_id = o.order_id

WHERE o.order_status = 'delivered'

GROUP BY p.payment_type