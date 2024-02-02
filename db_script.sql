CREATE DATABASE products_db;

\c products_db;

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(32),
    seller_id INTEGER,
    item_category INTEGER CHECK (item_category >= 0 AND item_category <= 9),
    keywords VARCHAR(8) [], 
    condition VARCHAR(10) CHECK (condition IN ('New', 'Used')),
    sale_price DECIMAL,
    quantity INTEGER CHECK (quantity >= 0), 
    thumbs_up_count INTEGER DEFAULT 0 CHECK (thumbs_up_count >= 0),
    thumbs_down_count INTEGER DEFAULT 0 CHECK (thumbs_down_count >= 0),
    CHECK (array_length(keywords, 1) <= 5)
);

-- INSERT INTO product(item_name, seller_id, item_category,keywords, condition, sale_price, quantity) VALUES ('Bose Headphones', 2, 0,  ARRAY['music'], 'Used', 300.00, 3);
-- INSERT INTO product(item_name, seller_id, item_category,keywords, condition, sale_price, quantity) VALUES ('Carpet', 8, 1, ARRAY['home', 'decor'], 'New', 200.00, 1);
-- INSERT INTO product(item_name, seller_id, item_category,keywords, condition, sale_price, quantity) VALUES ('Blender', 1, 2, ARRAY['kitchen','blender'], 'Used', 20.00, 1);

CREATE DATABASE customers_db;

\c customers_db;

CREATE TABLE seller (
    id SERIAL PRIMARY KEY,
    username VARCHAR(32) NOT NULL,
    password VARCHAR(12) CHECK(char_length(password) BETWEEN 6 and 12),
    thumbs_up_count INTEGER DEFAULT 0,
    thumbs_down_count INTEGER DEFAULT 0,
    items_sold INTEGER DEFAULT 0
    );

CREATE TABLE buyer (
    buyer_id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    no_of_items_purchased INTEGER DEFAULT 0,
    username VARCHAR(32) UNIQUE NOT NULL,
    password VARCHAR(12) CHECK (char_length(password) BETWEEN 6 AND 12),
    is_logged_in BOOLEAN DEFAULT FALSE
);

INSERT INTO buyer(name, username, password) VALUES ('Katie', 'katie', 'testkatie');
INSERT INTO buyer(name, username, password) VALUES ('Jeff', 'jeff', 'jeffbass');
INSERT INTO buyer(name, username, password) VALUES ('Mathew', 'mathew', 'mat490');

CREATE TABLE cart (
    cart_id SERIAL PRIMARY KEY,
    buyer_id INTEGER NOT NULL,
    status VARCHAR(10) NOT NULL CHECK (status IN ('Inprogress', 'Purchased')),
    status_changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (buyer_id) REFERENCES buyer(buyer_id)
);

INSERT INTO cart(buyer_id, status, status_changed_at) VALUES (2, 'Purchased', '2024-01-29 10:27:48.206506');
INSERT INTO cart(buyer_id, status, status_changed_at) VALUES (1, 'Inprogress', '2024-01-31 04:46:44.613737');

CREATE TABLE cart_items (
    cart_item_id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    feedback BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (cart_id) REFERENCES cart(cart_id)
);

INSERT INTO cart_items(cart_id, product_id, quantity) VALUES (1, 1, 1);
INSERT INTO cart_items(cart_id, product_id, quantity) VALUES (2, 1, 10);
INSERT INTO cart_items(cart_id, product_id, quantity) VALUES (2, 2, 3);

