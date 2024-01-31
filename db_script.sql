CREATE DATABASE products_db;

\c products_db;

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(32),
    item_category INTEGER CHECK (item_category >= 0 AND item_category <= 9),
    keywords VARCHAR(8) [],  
    condition VARCHAR(10) CHECK (condition IN ('New', 'Used')),
    sale_price DECIMAL,
    quantity INTEGER CHECK (quantity >= 0),
    seller_id INTEGER,
    thumbs_up_count INTEGER DEFAULT 0 CHECK (thumbs_up_count >= 0),
    thumbs_down_count INTEGER DEFAULT 0 CHECK (thumbs_down_count >= 0),
    CHECK (array_length(keywords, 1) <= 5)
);

-- INSERT INTO product(item_name, item_category, keywords, condition, sale_price) VALUES ('Dell', 0, ARRAY['portable', 'laptop'], 'Used', 619.99);
-- INSERT INTO product(item_name, item_category, keywords, condition, sale_price) VALUES ('Macbook Air', 0, ARRAY['portable', 'laptop','macbook'], 'New', 1499.99);

CREATE DATABASE customers_db;

\c customers_db;

CREATE TABLE buyer (
    buyer_id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    no_of_items_purchased INTEGER NOT NULL CHECK (items_purchased >= 0),
    username VARCHAR(32) UNIQUE NOT NULL,
    password VARCHAR(12) CHECK (char_length(password) BETWEEN 6 AND 12),
    is_logged_in BOOLEAN DEFAULT FALSE
);

-- INSERT INTO buyer(name, no_of_items_purchased, password) VALUES ('Katie', 0, 'testkatie');
-- INSERT INTO buyer(name, no_of_items_purchased, password) VALUES ('Jeff', 0, 'jeffbass');

CREATE TABLE cart (
    cart_id SERIAL PRIMARY KEY,
    buyer_id INTEGER NOT NULL,
    status VARCHAR(10) NOT NULL CHECK (status IN ('Inprogress', 'Purchased')),
    status_changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES buyer(buyer_id)
);

CREATE TABLE cart_items (
    cart_item_id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    feedback BOOLEAN DEFAULT NULL,
    FOREIGN KEY (cart_id) REFERENCES cart(cart_id)
);

-- UPDATE cart SET status = 'Purchased' where buyer_id = 2;

