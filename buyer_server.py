import socket
import threading
import time
from flask import Flask, request, Response, jsonify
import os
from products_db_model import ProductsDatabase
from customers_db_model import CustomersDatabase
from dotenv import load_dotenv
# import spyne_application
from zeep import Client

load_dotenv()

app = Flask(__name__)

customers_db = CustomersDatabase()
products_db = ProductsDatabase()

@app.route('/createaccount', methods = ['POST'])
def handle_create_account():
    data = request.json
    username = data['username']
    password = data['password']
    name = data['name']
    result = customers_db.create_account(username, password, name)
    if "Account created successfully" in result:
        return jsonify({"message": result}), 200
    else:
        return jsonify({"message": result}), 401

@app.route('/login', methods = ['POST'])
def handle_login():
    data = request.json
    username = data['username']
    password = data['password']
    result = customers_db.login(username, password)
    if "Login successful" in result:
        buyer_id = customers_db.get_buyer_id(username)
        customers_db.set_login_state(buyer_id, True)
        return jsonify({"message": result, "buyer_id": buyer_id}), 200
    else:
        return jsonify({"message": result}), 401

@app.route('/search', methods = ['POST'])
def handle_search():
    print("In search fn in server...")
    data = request.json
    item_category = data['item_category']
    keywords = data['keywords']
    print(f"Keywords in server: {keywords}")
    result = products_db.search_products(item_category, [keywords])
    header = "Id Name Condition Sale_price Quantity"
    formatted_results = "\n".join([header] + [f"{product[0]} {product[1]} {product[5]} {product[6]} {product[7]}" for product in result])
    print(f"Formatted results: {formatted_results}")
    return jsonify({"message": formatted_results}), 200
    
@app.route('/additem', methods = ['POST'])
def handle_add_to_cart():
    data = request.json
    buyer_id = data['buyer_id']
    product_id = data['product_id']
    quantity = data['quantity']
    result = customers_db.add_to_cart(buyer_id, product_id, quantity)
    if "Item is added to the cart successfully" in result:
        return jsonify({"message": result}), 200
    else:
        return jsonify({"message": "Error adding an item to the cart"}), 401

@app.route('/removeitem', methods = ['POST'])
def handle_remove_item_from_cart():
    data = request.json
    buyer_id = data['buyer_id']
    product_id = data['product_id']
    quantity = data['quantity']
    result = customers_db.remove_item_from_cart(buyer_id, product_id, quantity)
    if "Item removed from cart" in result:
        return jsonify({"message": result}), 200
    else:
        return jsonify({"message": result}), 401

@app.route('/clearcart', methods = ['POST'])
def handle_clear_cart():
    data = request.json
    buyer_id = data['buyer_id']
    result = customers_db.clear_cart(buyer_id)
    if "Cart cleared" in result:
        return jsonify({"message": result}), 200
    else:
        return jsonify({"message": result}), 401

@app.route('/displaycart', methods = ['GET'])
def handle_display_cart():
    data = request.json
    buyer_id = data['buyer_id']
    cart_items = customers_db.display_cart(buyer_id)
    if not cart_items:
        return jsonify({"message": "Your cart is empty"}), 200
    cart_display = []
    for product_id, quantity in cart_items:
        product_detail = products_db.get_product_details(product_id)
        if product_detail:
            item_name = product_detail[product_id]['name']
            sale_price = product_detail[product_id]['price']
            cart_display.append(f"Product: {item_name}, Quantity: {quantity}, Unit Price: {sale_price}, Total price: {sale_price*quantity}")
    formatted_cart = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(cart_display))
    if formatted_cart:
        return jsonify({"message": formatted_cart}), 200
    else:
        return jsonify({"message": "Error retrieving cart items"}), 401

@app.route('/sellerrating', methods = ['GET'])
def handle_get_seller_rating():
    data = request.json
    seller_id = data['seller_id']
    rating = customers_db.get_seller_rating(seller_id)
    if rating is not None:
        result = f"Seller Rating: Thumbs Up Count - {rating[0][0]}, Thumbs Down Count - {rating[0][1]}"
        return jsonify({"message": result}), 200
    else:
        return jsonify({"message": "Error getting seller rating"}), 401
    
def purchase_items(buyer_id):
    try:
        ordered_items = customers_db.get_purchased_items(buyer_id)
        if not ordered_items:
            return "No purchase was made."
            
        cart_display = []
        for product_id, quantity in ordered_items:
            product_detail = products_db.get_product_details(product_id)
            if product_detail:
                item_name = product_detail[product_id]['name']
                sale_price = product_detail[product_id]['price']
                cart_display.append(f"Product Id: {product_id}, Name: {item_name}, Quantity: {quantity}, Unit Price: {sale_price}, Total price: {sale_price*quantity}")

        formatted_cart = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(cart_display))
        return formatted_cart
    except Exception as e:
        print(f"Error sending purchased items: {e}")

@app.route('/purchasehistory', methods = ['GET'])
def handle_purchase_history():
    data = request.json
    buyer_id = data['buyer_id']
    ordered_items = purchase_items(buyer_id)
    if ordered_items:
        return jsonify({"message": ordered_items}), 200
    else:
        return jsonify({"message": "Error retrieving purchase history"}), 401  

@app.route('/provide_feedback', methods = ['POST'])
def handle_provide_feedback():
    data = request.json
    buyer_id = data['buyer_id']
    product_id = data['product_id']
    feedback_type = data['feedback_type']
    print(f"[SERVER] BuyerId: {buyer_id}, product_id: {product_id}, feedback_type: {feedback_type}")
    # Check if feedback has already been provided for this product
    if customers_db.has_provided_feedback(buyer_id, product_id):
        return jsonify({"message": "Feedback already provided for this product."}), 400
    
    cart_item_update_result = customers_db.update_feedback(buyer_id, product_id)
    feedback_result = products_db.update_feedback(product_id, feedback_type)

    seller_id = products_db.get_seller_id(product_id)
    seller_update_result = customers_db.update_seller_feedback(seller_id, feedback_type)

    if feedback_result and cart_item_update_result and seller_update_result:
        return jsonify({"message": "Feedback updated successfully."}), 200
    else:
        return jsonify({"error": "Failed to update feedback."}), 500

@app.route('/makepurchase', methods = ['POST'])
def handle_make_purchase():
    data = request.json
    print(f"Data in server..: {data}")
    buyer_id = data['buyer_id']
    name = data['name']
    credit_card_number = data['credit_card_number']
    expiration_date = data['expiration_date']
    soap_client = Client('http://localhost:8000/?wsdl')
    response = soap_client.service.make_purchase(id=buyer_id, name = name, credit_card_number=credit_card_number, expiration_date=expiration_date)

    # response = spyne_application.make_purchase(buyer_id, credit_card_number, expiration_date)
    print(f"Make Purchase Response: {response}")
    if response:
        return jsonify({"message": response}), 200
    else:
        return jsonify({"message": "Error making the payment"}), 401  

@app.route('/logout', methods = ['POST'])
def handle_logout():
    data = request.json
    buyer_id = data['buyer_id']
    result = customers_db.set_login_state(buyer_id, False)
    if "Update successful" in result:
        return jsonify({"message": "Logout successful"}), 200
    else:
        return jsonify({"message": "Logout failed"}), 401  
    
    # def handle_inactivity(self, buyer_id, conn):
    #     print("Handling inactivity...")
    #     self.handle_logout(buyer_id, conn)


    # def handle_client(self, conn, addr):
    #     print(f"[NEW CONNECTION] {addr} connected.")
    #     connected = True

    #     inactivityTimer = time.time()

    #     while connected:
    #         try:
    #             msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
    #             if msg_length:
    #                 msg_length = int(msg_length)
    #                 msg = conn.recv(msg_length).decode(self.FORMAT)
    #                 print(f"Message in [Server]: {msg}")

    #                 # inactivity check
    #                 previoustime = inactivityTimer
    #                 inactivityTimer = time.time()
                    
    #                 if msg.startswith("CREATE_ACCOUNT"):
    #                     _, username, password, name = msg.split()
    #                     self.handle_create_account(username, password, name, conn)
    #                 elif msg.startswith("LOGIN"):
    #                     _, username, password = msg.split()
    #                     self.handle_login(username, password, conn)
    #                 elif(inactivityTimer - previoustime > 20):
    #                     print("Should log out now")
    #                     self.handle_inactivity(msg.split()[1], conn)
    #                 elif msg.startswith("SEARCH"):
    #                     msg_split = msg.split()
    #                     item_category = msg_split[1]
    #                     keywords = msg_split[2:]
    #                     # print(f"Item_category: {item_category} and Keywords: {keywords}")
    #                     self.handle_search(item_category, keywords, conn)
    #                 elif msg.startswith("ADD_TO_CART"):
    #                     _, buyer_id, product_id, quantity = msg.split()
    #                     self.handle_add_to_cart(buyer_id, product_id, quantity, conn)
    #                 elif msg.startswith("REMOVE_ITEM_FROM_CART"):
    #                     _, buyer_id, product_id, quantity = msg.split()
    #                     self.handle_remove_item_from_cart(buyer_id, product_id, quantity, conn)
    #                 elif msg.startswith("CLEAR_CART"):
    #                     buyer_id = msg.split("CLEAR_CART ")[1]
    #                     self.handle_clear_cart(buyer_id, conn)
    #                 elif msg.startswith("DISPLAY_CART"):
    #                     buyer_id = msg.split("DISPLAY_CART ")[1]
    #                     self.handle_display_cart(buyer_id, conn)
    #                 elif msg.startswith("GET_SELLER_RATING"):
    #                     seller_id = msg.split("GET_SELLER_RATING ")[1]
    #                     self.handle_get_seller_rating(seller_id, conn)
    #                 elif msg.startswith("PURCHASE_HISTORY"):
    #                     buyer_id = msg.split("PURCHASE_HISTORY ")[1]
    #                     self.handle_purchase_history(buyer_id, conn)
    #                 elif msg.startswith("PROVIDE_FEEDBACK"):
    #                     buyer_id = msg.split("PROVIDE_FEEDBACK ")[1]
    #                     self.handle_provide_feedback(buyer_id, conn)
    #                 elif msg.startswith("LOGOUT"):
    #                     _, buyer_id = msg.split()
    #                     self.handle_logout(buyer_id, conn)
    #                 elif msg == self.DISCONNECT_MSG:
    #                     print("[In server] Disconnecting...")
    #                     connected = False
    #                 print(f'[{addr}] {msg}')
    #         except Exception as e:
    #             print(f"An error occurred: {e}")
    #             connected = False 

    #     conn.close()

if __name__ == "__main__":
    app.run(debug=True, host=os.getenv("HOST", "0.0.0.0"), port=int(os.getenv("PORT")) )
    
