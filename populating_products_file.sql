USE shop_project;

# Populating the Products table with 10 laptops
INSERT INTO products (name, price, stock) VALUES
('Manchester United Home Jersey 2024/25', 89.99, 20),
('Real Madrid Away Jersey 2024/25', 84.99, 15),
('FC Barcelona Third Jersey 2024/25', 79.99, 18),
('Liverpool Home Jersey 2024/25', 89.99, 25),
('Chelsea Away Jersey 2024/25', 84.99, 22),
('Bayern Munich Home Jersey 2024/25', 92.99, 20),
('Paris Saint-Germain Home Jersey 2024/25', 95.99, 17),
('Juventus Away Jersey 2024/25', 88.99, 19),
('Arsenal Third Jersey 2024/25', 82.99, 21),
('AC Milan Home Jersey 2024/25', 90.99, 16);

# Viewing the Products table
SELECT name FROM shop_project.products;

# Viewing the Products table
SELECT * FROM shop_project.customers;

# Viewing the orders table
SELECT * FROM shop_project.orders;

# Viewing the order_items table
SELECT * FROM shop_project.order_items;


SELECT Customer_id 
            FROM shop_project.customers
            WHERE Email = "test3";