import psycopg2
import os
from psycopg2 import OperationalError, Error
from dotenv import load_dotenv

load_dotenv()

class CustomersDatabase:
    def __init__(self):
        try:
            pw = os.getenv('PASSWORD')
            un = os.getenv('USER_NAME')
            self.DB_HOST = 'localhost'
            self.DB_PORT = '5432'
            self.DB_NAME = 'customers_db'
            self.connection = psycopg2.connect(database=self.DB_NAME, user=un, password=pw, host=self.DB_HOST, port=self.DB_PORT)
            self.cursor = self.connection.cursor()
        except OperationalError as e:
            print(f"An error occurred while connecting to the database: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    def create_account(self, username, password, name):
        try:
            self.cursor.execute("INSERT INTO buyer (name, no_of_items_purchased, password, username) VALUES (%s, %s, %s, %s)", (name, 0, password, username))
            self.connection.commit()
            return "Account created successfully."
        except Exception as e:
            self.connection.rollback()
            print(f"Error creating account: {e}")
            return "Error while creating account."

    def login(self, username, password):
        try:
            self.cursor.execute("SELECT password FROM buyer WHERE username = %s", (username,))
            stored_password = self.cursor.fetchone()
            if stored_password and stored_password[0] == password:
                return "Login successful"
            else:
                return "Login Failed. Invalid username or password."
        except Exception as e:
            print(f"Error during authentication: {e}")
            return "Authentication error."
    
    def set_login_state(self, buyer_id, state):
        try:
            self.cursor.execute("UPDATE buyer SET is_logged_in = %s WHERE buyer_id = %s", (state, buyer_id))
            self.connection.commit()
            return "Update successful"
        except Exception as e:
            self.connection.rollback()
            print(f"Error updating login state: {e}")

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
        
        # 3. Check if the item is already in the cart
        self.cursor.execute("SELECT quantity FROM cart_items WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
        existing_product = self.cursor.fetchone()

        if existing_product:
            self.cursor.execute("UPDATE cart_items SET quantity = quantity + %s WHERE cart_id = %s AND product_id = %s", (quantity, cart_id, product_id))
        else:
            self.cursor.execute("INSERT INTO cart_items (cart_id, product_id, quantity) VALUES (%s, %s, %s)", (cart_id, product_id, quantity))
        self.connection.commit()
        return "Item is added to the cart successfully"
    
    def remove_item_from_cart(self, buyer_id, product_id, quantity):
        try:
            self.cursor.execute("SELECT cart_id FROM cart WHERE buyer_id = %s AND status = 'Inprogress'", (buyer_id,))
            cart = self.cursor.fetchone()

            if cart is None:
                print(f"No active cart found for buyer_id: {buyer_id}")
                return f"No active cart found for buyer_id: {buyer_id}"

            cart_id = cart[0]
            self.cursor.execute("SELECT quantity FROM cart_items WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
            current_quantity = self.cursor.fetchone()[0]
            expected_quantity = current_quantity - int(quantity)
            if expected_quantity >= 1 :
                print("Updating the table...")
                self.cursor.execute("UPDATE cart_items SET quantity = quantity - %s WHERE cart_id = %s AND product_id = %s", (quantity, cart_id, product_id))
                self.connection.commit()
                return "Item removed from cart."
            elif expected_quantity == 0:
                print("Deleting a row in the table...")
                self.cursor.execute("DELETE FROM cart_items WHERE cart_id = %s AND product_id = %s", (cart_id, product_id))
                self.connection.commit()
                return "Item removed from cart."
            else:
                print(f"Trying to remove more than the available quantity {current_quantity} for the product {product_id}")
                return f"Trying to remove more than the available quantity {current_quantity} for the product {product_id}"
        except Exception as e:
            print(f"Error removing item from cart: {e}")
            self.connection.rollback()

    def clear_cart(self, buyer_id):
        try: 
            self.cursor.execute("SELECT cart_id FROM cart WHERE buyer_id = %s AND status = 'Inprogress'", (buyer_id,))
            cart = self.cursor.fetchone()

            if cart is None:
                print(f"No active cart found for buyer_id: {buyer_id}")
                return f"No active cart found for buyer_id: {buyer_id}"

            cart_id = cart[0]
            # print(f"Cart Id: {cart_id}")
            self.cursor.execute("DELETE FROM cart_items WHERE cart_id = %s", (cart_id,))
            self.cursor.execute("DELETE FROM cart WHERE cart_id = %s", (cart_id,))
            self.connection.commit()
            return "Cart cleared."
        except Exception as e:
            print(f"Error clearing the cart: {e}")
            self.connection.rollback()

    def display_cart(self, buyer_id):
        try:
            self.cursor.execute("SELECT product_id, quantity FROM cart_items WHERE cart_id IN (SELECT cart_id FROM cart WHERE buyer_id = %s AND status = 'Inprogress')", (buyer_id,))
            cart_items = self.cursor.fetchall()
            return cart_items
        except Exception as e:
            print(f"Error displaying the cart: {e}")
            self.connection.rollback()
            return None

    def get_seller_rating(self, seller_id):
        try:
            self.cursor.execute("SELECT thumbs_up_count, thumbs_down_count FROM seller WHERE id = %s", (seller_id,))
            rating = self.cursor.fetchall()
            return rating
        except Exception as e:
            print(f"Error getting seller rating: {e}")
            return None
    
    def get_purchased_items(self, buyer_id):
        try:
            self.cursor.execute("SELECT cart_id FROM cart WHERE buyer_id = %s AND status = 'Purchased' ORDER BY status_changed_at DESC LIMIT 1", (buyer_id,))
            latest_order = self.cursor.fetchone()
            if latest_order is None:
                print(f"No purchase made from buyer_id: {buyer_id}")
                return
            
            cart_id = latest_order[0]
            print(f"Cart Id: {cart_id}")

            # Fetch items in the latest order
            self.cursor.execute("SELECT product_id, quantity FROM cart_items WHERE cart_id = %s", (cart_id,))
            order_items = self.cursor.fetchall()
            return order_items
        except Exception as e:
            print(f"Error fetching the purchased items: {e}")
            return None
            
    def has_provided_feedback(self, buyer_id, product_id):
        try:
            self.cursor.execute("SELECT feedback FROM cart_items WHERE product_id = %s AND cart_id IN (SELECT cart_id FROM cart WHERE buyer_id = %s AND status = 'Purchased' ORDER BY status_changed_at DESC LIMIT 1)", (product_id, buyer_id))
            feedback = self.cursor.fetchone()[0] 
            print(f"Feedback in [DB]: {feedback}")
            return feedback
        except Exception as e:
            print(f"Error checking feedback status: {e}")
            return False
    
    def update_feedback(self, buyer_id, product_id):
        try:
            self.cursor.execute("UPDATE cart_items SET feedback = True WHERE product_id = %s AND cart_id IN (SELECT cart_id FROM cart WHERE buyer_id = %s AND status = 'Purchased' ORDER BY status_changed_at DESC LIMIT 1)", (product_id, buyer_id))
            self.connection.commit()
            return "Feedback updated successfully."
        except Exception as e:
            self.connection.rollback()
            print(f"Error while updating feedback: {e}")
            return False
    
    def update_seller_feedback(self, seller_id, feedback_type):
        try:
            column_to_increment = 'thumbs_up_count' if feedback_type == '1' else '2'
            self.cursor.execute(f"UPDATE seller SET {column_to_increment} = (SELECT {column_to_increment} FROM seller WHERE id = %s) + 1 WHERE id = %s", (seller_id, seller_id))
            self.connection.commit()
            return "Feedback updated successfully."
        except Exception as e:
            self.connection.rollback()
            print(f"Error while updating feedback in seller: {e}")
            return False
    
    def get_buyer_id(self, username):
        try:
            self.cursor.execute("SELECT buyer_id FROM buyer WHERE username = %s", (username,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error fetching buyer_id: {e}")
            return None

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

