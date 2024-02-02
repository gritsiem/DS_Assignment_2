import psycopg2
from psycopg2 import OperationalError, Error

class ProductsDatabase:
    def __init__(self, dbname, user, password, host, port):
        try:
            self.connection = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)
            self.cursor = self.connection.cursor()
        except OperationalError as e:
            print(f"An error occurred while connecting to the database: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def search_products(self, query):
        try:
            # self.cursor.execute("SELECT * FROM product WHERE item_name ILIKE %s OR keywords ILIKE %s", ('%'+query+'%', '%'+query+'%'))
            self.cursor.execute("SELECT * FROM product WHERE item_name ILIKE %s OR %s = ANY(keywords)", ('%'+query+'%', query))
            return self.cursor.fetchall()
        except OperationalError as e:
            print(f"An error occurred while executing the query: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    # def insert_product(self, name, category, keywords, condition, price):
    #     try:
    #         self.cursor.execute("INSERT INTO product (item_name, item_category, keywords, condition, sale_price) VALUES (%s, %s, %s, %s, %s)", (name, category, keywords, condition, price))
    #         self.connection.commit()
    #     except psycopg2.Error as e:
    #         print(f"Database error: {e}")
    #     except Exception as e:
    #         print(f"An unexpected error occurred: {e}")
    
    def add_to_cart(self, buyer_id, product_id, quantity):
        # 1. Check if the buyer already has an Inprogress cart
        self.cursor.execute("SELECT cart_id FROM cart WHERE buyer_id = %s AND status = 'Inprogress'", (buyer_id,))
        cart = self.cursor.fetchone()
        
        # 2. If not, create a new cart
        if not cart:
            self.cursor.execute("INSERT INTO cart (buyer_id, status) VALUES (%s, 'Inprogress') RETURNING cart_id", (buyer_id,))
            cart_id = self.cursor.fetchone()[0]
        else:
            cart_id = cart[0]
        
        # 3. Add the item to the cart_items table
        self.cursor.execute("INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s, %s, %s)", (cart_id, product_id, quantity))
        self.connection.commit()
    
    def get_product_details(self, product_id):
        try:
            # self.cursor.execute("SELECT product_id, item_name, sale_price FROM product WHERE id = %s", (product_id,))
            # product_details = self.cursor.fetchall()
            # return product_details

            # Create a string with placeholders for product_ids
            # placeholders = ','.join(['%s'] * len(product_ids))
            # Execute the query with the list of product_ids
            self.cursor.execute(f"SELECT id, item_name, sale_price FROM product WHERE id = %s", (product_id,))
            product_details = self.cursor.fetchall()
            return {product_id: {'name': name, 'price': price} for product_id, name, price in product_details}
        except Exception as e:
            print(f"Error while fetching the product details: {e}")
            return None

    def update_feedback(self, product_id, feedback_type):
        try:
            column_to_increment = 'thumbs_up_count' if feedback_type == '1' else '2'
            self.cursor.execute(f"UPDATE product SET {column_to_increment} = (SELECT {column_to_increment} FROM product WHERE id = %s) +1 WHERE id = %s", (product_id,product_id))
            self.connection.commit()
            return "Feedback updated successfully."
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating feedback: {e}")
            return False
    
    def get_seller_id(self, product_id):
        try:
            self.cursor.execute(f"SELECT seller_id FROM product WHERE id = %s", (product_id,))
            seller_id = self.cursor.fetchone()[0]
            return seller_id
        except Exception as e:
            print(f"Error while fetching seller_id: {e}")
            return None

    def product_is_present(self, product_id):
        try:
            self.cursor.execute(f"")  ##finish this
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating feedback: {e}")
            return "Error while updating feedback."

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

