SELECT
    o.order_id,
    o.customer_id,
    c.customer_state,
    r.review_score,
    DATE(o.order_purchase_timestamp) AS purchase_date,
    DATE(o.order_delivered_customer_date) AS actual_delivery_date,
    DATE(o.order_estimated_delivery_date) AS estimated_delivery_date,
    ROUND(JULIANDAY(o.order_delivered_customer_date) - JULIANDAY(o.order_purchase_timestamp), 1) AS actual_delivery_days,
    ROUND(JULIANDAY(o.order_delivered_customer_date) - JULIANDAY(o.order_estimated_delivery_date), 1) AS delay_days,
    CASE
        WHEN JULIANDAY(o.order_delivered_customer_date) > JULIANDAY(o.order_estimated_delivery_date)
        THEN 'Delayed'
        ELSE 'On-Time'
    END AS delivery_status
FROM olist_orders o
JOIN olist_order_reviews r ON o.order_id = r.order_id
JOIN olist_customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL;