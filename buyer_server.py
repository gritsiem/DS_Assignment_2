import socket
import threading
import time
from products_db_model import ProductsDatabase
from customers_db_model import CustomersDatabase

class BuyerServer:

    def __init__(self):
        self.HEADER = 1024
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MSG = "!DISCONNECT"
        self.server_ip = self.get_local_ip()
        self.address = (self.server_ip, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.address)
        self.customers_db = CustomersDatabase()
        self.products_db = ProductsDatabase()
        self.start()

    @staticmethod
    def get_local_ip():
        try:
            # Attempt to connect to an arbitrary public IP address.
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            print(f"Error: {e}")
            return None

    def handle_create_account(self, username, password, name, conn):
        try:
            result = self.customers_db.create_account(username, password, name)
            conn.send(result.encode(self.FORMAT))
        except Exception as e:
            print(f"Error creating account: {e}")
            conn.send("Failed to create account.".encode(FORMAT))


    def handle_login(self, username, password, conn):
        try:
            result = self.customers_db.login(username, password)
            conn.send(result.encode(self.FORMAT))
            if "Login successful" in result:
                buyer_id = self.customers_db.get_buyer_id(username)
                self.customers_db.set_login_state(buyer_id, True)
                conn.send(f"Your buyer ID is {buyer_id}".encode(self.FORMAT))
            else:
                conn.send("Login failed".encode(self.FORMAT))
        except Exception as e:
            print(f"Error during authentication: {e}")
            conn.send("Authentication failed.".encode(self.FORMAT))

    def handle_search(self, item_category, keywords, conn):
        try:
            results = self.products_db.search_products(item_category, keywords)
            header = "Id Name Condition Sale_price Quantity"
            formatted_results = "\n".join([header] + [f"{product[0]} {product[1]} {product[5]} {product[6]} {product[7]}" for product in results])
            conn.send(formatted_results.encode(self.FORMAT))
        except Exception as e:
            print(f"Error during search: {e}")
            conn.send("An error occurred while searching for products.".encode(self.FORMAT))

    def handle_add_to_cart(self, buyer_id, product_id, quantity, conn):
        try:
            self.products_db.product_is_present(product_id)
            self.customers_db.add_to_cart(buyer_id, product_id, quantity)
            conn.send("Item added to cart.".encode(self.FORMAT))
        except Exception as e:
            print(f"Error adding to cart: {e}")
            conn.send("Failed to add item to cart.".encode(self.FORMAT))

    def handle_remove_item_from_cart(self, buyer_id, product_id, quantity, conn):
        try:
            resp = self.customers_db.remove_item_from_cart(buyer_id, product_id, quantity)
            conn.send(resp.encode(self.FORMAT))
        except Exception as e:
            print(f"Error removing item from cart: {e}")
            conn.send("Failed to remove item from cart.".encode(self.FORMAT))

    def handle_clear_cart(self, buyer_id, conn):
        try:
            self.customers_db.clear_cart(buyer_id)
            conn.send("Cart cleared.".encode(self.FORMAT))
        except Exception as e:
            print(f"Error in clearing the cart: {e}")
            conn.send("Failed to clear the cart.".encode(self.FORMAT))

    def handle_display_cart(self, buyer_id, conn):
        try: 
            cart_items = self.customers_db.display_cart(buyer_id)
            if not cart_items:
                conn.send("Your cart is empty.".encode(self.FORMAT))
                return
            print(f"Cart Items: {cart_items}")
            cart_display = []
            for product_id, quantity in cart_items:
                product_detail = self.products_db.get_product_details(product_id)
                if product_detail:
                    item_name = product_detail[product_id]['name']
                    sale_price = product_detail[product_id]['price']
                    cart_display.append(f"Product: {item_name}, Quantity: {quantity}, Unit Price: {sale_price}, Total price: {sale_price*quantity}")
            formatted_cart = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(cart_display))
            conn.send(formatted_cart.encode(self.FORMAT))
        except Exception as e:
            print(f"Error sending cart contents: {e}")
            conn.send("Failed to retrieve cart contents.".encode(self.FORMAT))

    def handle_get_seller_rating(self, seller_id, conn):
        try:
            rating = self.customers_db.get_seller_rating(seller_id)
            print(f"Rating: {rating}")
            if rating is not None:
                conn.send(f"Seller Rating: Thumbs Up Count - {rating[0][0]}, Thumbs Down Count - {rating[0][1]}".encode(self.FORMAT))
            else:
                conn.send("Seller rating not found.".encode(self.FORMAT))
        except Exception as e:
            print(f"Error sending seller rating: {e}")
            conn.send("Failed to retrieve seller rating.".encode(self.FORMAT))
    
    def purchase_items(self, buyer_id):
        try:
            ordered_items = self.customers_db.get_purchased_items(buyer_id)
            if not ordered_items:
                return "No purchase was made."
            
            cart_display = []
            for product_id, quantity in ordered_items:
                product_detail = self.products_db.get_product_details(product_id)
                if product_detail:
                    item_name = product_detail[product_id]['name']
                    sale_price = product_detail[product_id]['price']
                    cart_display.append(f"Product Id: {product_id}, Name: {item_name}, Quantity: {quantity}, Unit Price: {sale_price}, Total price: {sale_price*quantity}")

            formatted_cart = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(cart_display))
            return formatted_cart
        except Exception as e:
            print(f"Error sending purchased items: {e}")

    def handle_purchase_history(self, buyer_id, conn):
        ordered_items = self.purchase_items(buyer_id)
        conn.send(ordered_items.encode(self.FORMAT))

    def handle_provide_feedback(self, buyer_id, conn):
        try:
            purchased_items = self.purchase_items(buyer_id)
            print(f"Purchased Items: {purchased_items}")
            conn.send(purchased_items.encode(self.FORMAT))

            # conn.send("\nPlease enter the product ID for which you want to provide feedback:".encode(self.FORMAT))
            product_id = conn.recv(self.HEADER).decode(self.FORMAT)
        
            # Check if feedback has already been provided for this product
            if self.customers_db.has_provided_feedback(buyer_id, product_id):
                conn.send("\nFeedback already provided for this product.".encode(self.FORMAT))
                return

            # Get feedback type from the client
            conn.send("\nPlease enter your feedback \nChoose 1 for Thumbs Up or 2 for Thumbs Down:".encode(self.FORMAT))
            feedback_type = conn.recv(self.HEADER).decode(self.FORMAT)
        
            feedback_result = self.products_db.update_feedback(product_id, feedback_type)
            cart_item_update_result = self.customers_db.update_feedback(buyer_id, product_id)

            seller_id = self.products_db.get_seller_id(product_id)
            seller_update_result = self.customers_db.update_seller_feedback(seller_id, feedback_type)

            # if not (feedback_result and cart_item_update_result and seller_update_result):
            #     conn.send("Error updating feedback")
            conn.send(feedback_result.encode(self.FORMAT))
        except Exception as e:
            print(f"Error providing feedback: {e}")
            conn.send("Failed to update.".encode(self.FORMAT))

    def handle_logout(self, buyer_id, conn):
        try:
            self.customers_db.set_login_state(buyer_id, False)
            conn.send("Logout successful".encode(self.FORMAT))
        except Exception as e:
            print(f"Error during logout: {e}")
            conn.send("Logout failed.".encode(self.FORMAT))
    
    def handle_inactivity(self, buyer_id, conn):
        print("Handling inactivity...")
        self.handle_logout(buyer_id, conn)


    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected.")
        connected = True

        inactivityTimer = time.time()

        while connected:
            try:
                msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(self.FORMAT)
                    print(f"Message in [Server]: {msg}")
                    # inactivity check
                    previoustime = inactivityTimer
                    inactivityTimer = time.time()
                    if(inactivityTimer - previoustime > 20):
                        print("Should log out now")
                        self.handle_inactivity(msg.split()[1], conn)
                    elif msg.startswith("CREATE_ACCOUNT"):
                        _, username, password, name = msg.split()
                        self.handle_create_account(username, password, name, conn)
                    elif msg.startswith("LOGIN"):
                        _, username, password = msg.split()
                        self.handle_login(username, password, conn)
                    elif msg.startswith("SEARCH"):
                        msg_split = msg.split()
                        item_category = msg_split[1]
                        keywords = msg_split[2:]
                        # print(f"Item_category: {item_category} and Keywords: {keywords}")
                        self.handle_search(item_category, keywords, conn)
                    elif msg.startswith("ADD_TO_CART"):
                        _, buyer_id, product_id, quantity = msg.split()
                        self.handle_add_to_cart(buyer_id, product_id, quantity, conn)
                    elif msg.startswith("REMOVE_ITEM_FROM_CART"):
                        _, buyer_id, product_id, quantity = msg.split()
                        self.handle_remove_item_from_cart(buyer_id, product_id, quantity, conn)
                    elif msg.startswith("CLEAR_CART"):
                        buyer_id = msg.split("CLEAR_CART ")[1]
                        self.handle_clear_cart(buyer_id, conn)
                    elif msg.startswith("DISPLAY_CART"):
                        buyer_id = msg.split("DISPLAY_CART ")[1]
                        self.handle_display_cart(buyer_id, conn)
                    elif msg.startswith("GET_SELLER_RATING"):
                        seller_id = msg.split("GET_SELLER_RATING ")[1]
                        self.handle_get_seller_rating(seller_id, conn)
                    elif msg.startswith("PURCHASE_HISTORY"):
                        buyer_id = msg.split("PURCHASE_HISTORY ")[1]
                        self.handle_purchase_history(buyer_id, conn)
                    elif msg.startswith("PROVIDE_FEEDBACK"):
                        buyer_id = msg.split("PROVIDE_FEEDBACK ")[1]
                        self.handle_provide_feedback(buyer_id, conn)
                    elif msg.startswith("LOGOUT"):
                        _, buyer_id = msg.split()
                        self.handle_logout(buyer_id, conn)
                    elif msg == self.DISCONNECT_MSG:
                        print("[In server] Disconnecting...")
                        connected = False
                    print(f'[{addr}] {msg}')
            except Exception as e:
                print(f"An error occurred: {e}")
                connected = False 

        conn.close()

    def start(self):
        self.server.listen()
        print(f"[LISTENING] Server is listening on {self.server_ip}")
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn,addr))
            thread.start()
            print(f"[ACTIVE CONNECIONS] {threading.active_count() -1}")
            # Subtracted 1 because, server is running on 1 thread

if __name__ == "__main__":
    server = BuyerServer()
    
