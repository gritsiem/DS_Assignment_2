import socket
import threading
# import psycopg2
# from psycopg2 import sql
from products_db_model import ProductsDatabase
from customers_db_model import CustomersDatabase

HEADER = 2048
PORT = 5050

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
SERVER = get_local_ip()
# SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
# print(socket.gethostname())
ADDR  = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'products_db'
DB_NAME1 = 'customers_db'
DB_USER = 'naveenaganesan'
DB_PASSWORD = 'test1234'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

products_db = ProductsDatabase(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
customers_db = CustomersDatabase(dbname=DB_NAME1, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)

def handle_create_account(username, password, name, conn):
    try:
        result = customers_db.create_account(username, password, name)
        conn.send(result.encode(FORMAT))
    except Exception as e:
        print(f"Error creating account: {e}")
        conn.send("Failed to create account.".encode(FORMAT))

def handle_login(username, password, conn):
    try:
        result = customers_db.login(username, password)
        conn.send(result.encode(FORMAT))
        if "Login successful" in result:
            buyer_id = customers_db.get_buyer_id(username)
            customers_db.set_login_state(buyer_id, True)
            conn.send(f"Your buyer ID is {buyer_id}".encode(FORMAT))
        else:
            conn.send("Login failed".encode(FORMAT))
    except Exception as e:
        print(f"Error during authentication: {e}")
        conn.send("Authentication failed.".encode(FORMAT))

def handle_search(query, conn):
    try:
        results = products_db.search_products(query)
        formatted_results = "\n".join([f"{product[0]}. {product[1]}" for product in results])
        conn.send(formatted_results.encode(FORMAT))
    except Exception as e:
        print(f"Error during search: {e}")
        conn.send("An error occurred while searching for products.".encode(FORMAT))

def handle_add_to_cart(buyer_id, product_id, quantity, conn):
    try:
        products_db.product_is_present(product_id)
        customers_db.add_to_cart(buyer_id, product_id, quantity)
        conn.send("Item added to cart.".encode(FORMAT))
    except Exception as e:
        print(f"Error adding to cart: {e}")
        conn.send("Failed to add item to cart.".encode(FORMAT))

def handle_remove_item_from_cart(buyer_id, product_id, quantity, conn):
    try:
        resp = customers_db.remove_item_from_cart(buyer_id, product_id, quantity)
        conn.send(resp.encode(FORMAT))
        # conn.send("Item removed from cart.".encode(FORMAT))
    except Exception as e:
        print(f"Error removing item from cart: {e}")
        conn.send("Failed to remove item from cart.".encode(FORMAT))

def handle_clear_cart(buyer_id, conn):
    try:
        customers_db.clear_cart(buyer_id)
        conn.send("Cart cleared.".encode(FORMAT))
    except Exception as e:
        print(f"Error in clearing the cart: {e}")
        conn.send("Failed to clear the cart.".encode(FORMAT))

def handle_display_cart(buyer_id, conn):
    try: 
        cart_items = customers_db.display_cart(buyer_id)
        if not cart_items:
            conn.send("Your cart is empty.".encode(FORMAT))
            return
        print(f"Cart Items: {cart_items}")
        cart_display = []
        for product_id, quantity in cart_items:
            product_detail = products_db.get_product_details(product_id)
            if product_detail:
                item_name = product_detail[product_id]['name']
                sale_price = product_detail[product_id]['price']
                cart_display.append(f"Product: {item_name}, Quantity: {quantity}, Unit Price: {sale_price}, Total price: {sale_price*quantity}")

        # formatted_cart = "\n".join(cart_display)
        formatted_cart = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(cart_display))
        conn.send(formatted_cart.encode(FORMAT))
    except Exception as e:
        print(f"Error sending cart contents: {e}")
        conn.send("Failed to retrieve cart contents.".encode(FORMAT))

def handle_get_seller_rating(seller_id, conn):
    try:
        rating = customers_db.get_seller_rating(seller_id)
        if rating is not None:
            conn.send(f"Seller Rating: {rating}".encode(FORMAT))
        else:
            conn.send("Seller rating not found.".encode(FORMAT))
    except Exception as e:
        print(f"Error sending seller rating: {e}")
        conn.send("Failed to retrieve seller rating.".encode(FORMAT))

def handle_purchase_history(buyer_id, conn):
    try:
        ordered_items = customers_db.get_purchased_items(buyer_id)
        if not ordered_items:
            conn.send("No purchase was made.".encode(FORMAT))
            return
            
        cart_display = []
        for product_id, quantity in ordered_items:
            product_detail = products_db.get_product_details(product_id)
            if product_detail:
                item_name = product_detail[product_id]['name']
                sale_price = product_detail[product_id]['price']
                cart_display.append(f"Product Id: {product_id}, Name: {item_name}, Quantity: {quantity}, Unit Price: {sale_price}, Total price: {sale_price*quantity}")

        formatted_cart = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(cart_display))

        conn.send(formatted_cart.encode(FORMAT))
    except Exception as e:
        print(f"Error sending purchased items: {e}")
        conn.send("Failed to retrieve purchased items.".encode(FORMAT))

def handle_provide_feedback(buyer_id, conn):
    try:
        # print("[Handling Feedback] in server....")
        purchased_items = handle_purchase_history(buyer_id, conn)
        conn.send(purchased_items.encode(FORMAT))
        conn.send("\nPlease enter the product ID for which you want to provide feedback:".encode(FORMAT))
        product_id = conn.recv(HEADER).decode(FORMAT)
        
        # Check if feedback has already been provided for this product
        if customers_db.has_provided_feedback(buyer_id, product_id):
            conn.send("\nFeedback already provided for this product.".encode(FORMAT))
            return

        # Get feedback type from the client
        conn.send("\nPlease enter your feedback (Thumbs Up or Thumbs Down):".encode(FORMAT))
        feedback_type = conn.recv(HEADER).decode(FORMAT)
        print(f"[FEEDBACK in Server]: {feedback_type}")

        feedback_result = products_db.update_feedback(product_id, feedback_type)
        conn.send(feedback_result.encode(FORMAT))

        # Provide feedback
        feedback_result = products_db.provide_feedback(product_id, feedback_type)
        conn.send(feedback_result.encode(FORMAT))

    except Exception as e:
        print(f"Error sending purchased items: {e}")
        conn.send("Failed to retrieve purchased items.".encode(FORMAT))

def handle_logout(buyer_id, conn):
    try:
        customers_db.set_login_state(buyer_id, False)
        conn.send("Logout successful".encode(FORMAT))
    except Exception as e:
        print(f"Error during logout: {e}")
        conn.send("Logout failed.".encode(FORMAT))

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT).strip()
            # buyer_id = 1
            # print(f"Received raw msg_length: '{msg_length}'") 
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg.startswith("CREATE_ACCOUNT"):
                    _, username, password, name = msg.split()
                    handle_create_account(username, password, name, conn)
                elif msg.startswith("LOGIN"):
                    _, username, password = msg.split()
                    handle_login(username, password, conn)
                elif msg.startswith("SEARCH"):
                    query = msg.split("SEARCH ")[1]
                    handle_search(query, conn)
                elif msg.startswith("ADD_TO_CART"):
                    _, buyer_id, product_id, quantity = msg.split()
                    handle_add_to_cart(buyer_id, product_id, quantity, conn)
                elif msg.startswith("REMOVE_ITEM_FROM_CART"):
                    # contents = msg.split()
                    # print(f"Contents: {contents}")
                    _, buyer_id, product_id, quantity = msg.split()
                    handle_remove_item_from_cart(buyer_id, product_id, quantity, conn)
                elif msg.startswith("CLEAR_CART"):
                    buyer_id = msg.split("CLEAR_CART ")[1]
                    handle_clear_cart(buyer_id, conn)
                elif msg.startswith("DISPLAY_CART"):
                    buyer_id = msg.split("DISPLAY_CART ")[1]
                    handle_display_cart(buyer_id, conn)
                elif msg.startswith("GET_SELLER_RATING"):
                    seller_id = msg.split("GET_SELLER_RATING ")[1]
                    handle_get_seller_rating(seller_id, conn)
                elif msg.startswith("PURCHASE_HISTORY"):
                    buyer_id = msg.split("PURCHASE_HISTORY ")[1]
                    handle_purchase_history(buyer_id, conn)
                elif msg.startswith("PROVIDE_FEEDBACK"):
                    buyer_id = msg.split("PROVIDE_FEEDBACK ")[1]
                    handle_provide_feedback(buyer_id, conn)
                elif msg.startswith("LOGOUT"):
                    _, buyer_id = msg.split()
                    handle_logout(buyer_id, conn)
                elif msg == DISCONNECT_MSG:
                    connected = False
                print(f'[{addr}] {msg}')
                # conn.send("Msg received...".encode(FORMAT))
        except Exception as e:
            print(f"An error occurred: {e}")
            connected = False 

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECIONS] {threading.active_count() -1}")
        # Subtracted 1 because, server is running on 1 thread

print("[STARTING] server is starting ...")
start()
