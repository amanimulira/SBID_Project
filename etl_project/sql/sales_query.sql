SELECT s.id, s.sale_date, s.quantity,
    c.name as customer_name, c.country,
    p.name as product_name, p.price
FROM sales s
JOIN customers c ON s.customer_id = c.id
JOIN products p ON s.product_id = p.id;