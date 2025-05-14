DROP DATABASE IF EXISTS chatbot;
CREATE DATABASE chatbot;
USE chatbot;

-- ✅ Users Table (For account-related queries)
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ✅ Orders Table (With modification & cancellation details)
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(255),
    email VARCHAR(255),
    order_status VARCHAR(50),
    tracking_number VARCHAR(50) UNIQUE, -- Ensuring unique tracking number
    order_date DATE, 
    delivery_date DATE, 
    items TEXT
);
ALTER TABLE orders 
ADD COLUMN cancellation_reason TEXT NULL,
ADD COLUMN modification_details TEXT NULL;

-- ✅ Order Tracking Table (For real-time tracking updates)
CREATE TABLE order_tracking (
    tracking_number VARCHAR(50) PRIMARY KEY,
    status_update TEXT NOT NULL,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tracking_number) REFERENCES orders(tracking_number) ON DELETE CASCADE
);


-- ✅ Payment Methods Table (With status)
CREATE TABLE payment_methods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    method VARCHAR(50) NOT NULL,
    status ENUM('Available', 'Unavailable') DEFAULT 'Available'
);

-- ✅ Shipping Info Table (More details added)
CREATE TABLE shipping_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    charge VARCHAR(50) NOT NULL,
    shipping_speed VARCHAR(50) NOT NULL,
    estimated_time VARCHAR(50) NOT NULL
);

-- ✅ Discounts Table
CREATE TABLE discounts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    description TEXT NOT NULL
);

-- ✅ Products Table (More details added)
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    sales INT DEFAULT 0,
    reviews TEXT
);

-- ✅ Return Policies Table
CREATE TABLE return_policies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    policy_text TEXT NOT NULL
);

-- ✅ Customer Support Table (For chatbot queries)
CREATE TABLE customer_support (
    id INT PRIMARY KEY AUTO_INCREMENT,
    query VARCHAR(255) NOT NULL,
    response TEXT NOT NULL
);

CREATE TABLE product_queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    queried_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE support_tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    issue_type VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE support_tickets
ADD COLUMN submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP;

CREATE TABLE chatbot_feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL,
    feedback VARCHAR(10) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



USE chatbot;
SELECT * FROM support_tickets;


SELECT product_name, COUNT(*) AS times_asked
FROM product_queries
GROUP BY product_name
ORDER BY times_asked DESC;
show tables;


-- 🛒 Insert Sample Orders (With tracking & cancellation details)
INSERT INTO orders (customer_name, email, order_status, tracking_number, order_date, delivery_date, items, cancellation_reason, modification_details) 
VALUES 
('Alice', 'alice@example.com', 'Shipped', 'TRK123456', '2025-03-10', '2025-03-17', 'Laptop, Mouse', NULL, NULL),
('Bob', 'bob@example.com', 'Processing', 'TRK654321', '2025-03-12', '2025-03-20', 'Smartphone, Earphones', NULL, 'Changed phone color to blue'),
('Charlie', 'charlie@example.com', 'Delivered', 'TRK789012', '2025-03-05', '2025-03-12', 'Book, Notebook', 'Customer changed mind', NULL),
('Diana', 'diana@example.com', 'Pending', 'TRK111111', '2025-04-01', '2025-04-08', 'Bluetooth Speaker', NULL, NULL),
('Ethan', 'ethan@example.com', 'Shipped', 'TRK222222', '2025-04-03', '2025-04-10', 'Wrist Watch', NULL, NULL),
('Fiona', 'fiona@example.com', 'Processing', 'TRK333333', '2025-04-04', '2025-04-11', 'Backpack', NULL, NULL),
('George', 'george@example.com', 'Delivered', 'TRK444444', '2025-03-28', '2025-04-04', 'Gaming Mouse', NULL, NULL),
('Hannah', 'hannah@example.com', 'Cancelled', 'TRK555555', '2025-03-30', '2025-04-06', 'Sunglasses', 'Out of stock', NULL),
('Ivan', 'ivan@example.com', 'Processing', 'TRK666666', '2025-04-02', '2025-04-09', 'Yoga Mat', NULL, 'Changed color to green'),
('Julia', 'julia@example.com', 'Shipped', 'TRK777777', '2025-04-05', '2025-04-12', 'AirPods Pro', NULL, NULL);


-- 🚚 Insert Order Tracking Details
INSERT INTO order_tracking (tracking_number, status_update) VALUES 
('TRK123456', 'Package is out for delivery'),
('TRK654321', 'Order is being packed'),
('TRK789012', 'Order delivered successfully'),
('TRK111111', 'Awaiting dispatch'),
('TRK222222', 'Shipped and en route to your city'),
('TRK333333', 'Being packed in warehouse'),
('TRK444444', 'Delivered to doorstep'),
('TRK555555', 'Cancelled before shipping'),
('TRK666666', 'Item is being prepared'),
('TRK777777', 'Package handed to courier');


-- 💳 Insert Payment Methods (With status)
INSERT INTO payment_methods (method, status) VALUES 
('Credit Card', 'Available'), 
('Debit Card', 'Available'), 
('PayPal', 'Available'), 
('Google Pay', 'Unavailable'), 
('Apple Pay', 'Available'), 
('Cash on Delivery', 'Available');

-- 🚢 Insert Shipping Info (More details added)
INSERT INTO shipping_info (charge, shipping_speed, estimated_time) VALUES 
('Free shipping on orders above $50', 'Standard', '5-7 business days'),
('$5 for express shipping', 'Express', '2-3 business days');

-- 🎉 Insert Discounts
INSERT INTO discounts (description) VALUES 
('10% off on first purchase'), 
('Buy 1 Get 1 Free on selected items'), 
('Flat $5 off on orders above $50');

-- 🏆 Insert Best-Selling Products (With category, stock, and reviews)
INSERT INTO products (name, category, price, stock, sales, reviews) VALUES 
('iPhone 15', 'Electronics', 999.99, 50, 5000, 'Amazing phone with great battery life'),
('Samsung Galaxy S23', 'Electronics', 899.99, 40, 4500, 'Super smooth display and great camera'),
('MacBook Air M2', 'Computers', 1299.99, 30, 3000, 'Lightweight and powerful, great for work'),
('Sony Headphones', 'Accessories', 199.99, 60, 2500, 'Excellent sound quality and noise cancellation'),
('Nike Running Shoes', 'Footwear', 149.99, 100, 2000, 'Very comfortable and durable');

-- 📜 Insert Return Policy
INSERT INTO return_policies (policy_text) VALUES 
('You can return products within 30 days of purchase. Items must be in original condition.');

-- 📞 Insert Customer Support Responses
INSERT INTO customer_support (query, response) VALUES 
('reset password', 'You can reset your password by clicking on the "Forgot Password" link on the login page.'),
('change email', 'To change your email, go to account settings and update your email address.'),
('contact support', 'You can contact customer support via our 24/7 chat or call us at +1-800-555-1234.'),
('unsubscribe emails', 'You can unsubscribe from emails in your account settings under "Notifications".');
