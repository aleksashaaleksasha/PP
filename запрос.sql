WITH 
product_cost AS (
    SELECT 
        p.product_id,
        p.name,
        SUM(sm.quantity * m.price) AS material_cost
    FROM products p
    JOIN specifications s ON p.product_id = s.product_id
    JOIN specification_materials sm ON s.specification_id = sm.specification_id
    JOIN materials m ON sm.material_id = m.material_id
    GROUP BY p.product_id, p.name
),
order_details AS (
    SELECT 
        o.order_id,
        o.customer_id,
        c.name AS customer_name,
        o.order_date,
        op.product_id,
        p.name,
        op.quantity AS order_quantity,
        pc.material_cost,
        (op.quantity * pc.material_cost) AS total_material_cost
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN order_products op ON o.order_id = op.order_id
    JOIN products p ON op.product_id = p.product_id
    JOIN product_cost pc ON op.product_id = pc.product_id
)

SELECT 
    order_id,
    customer_id,
    customer_name,
    order_date,
    SUM(total_material_cost) AS total_cost,
    SUM(order_quantity) AS total_products
FROM order_details
GROUP BY order_id, customer_id, customer_name, order_date
ORDER BY order_id;