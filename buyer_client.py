import socket
import time

class BuyerClient:

    def __init__(self):
        self.HEADER = 1024
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MSG = "!DISCONNECT"
        self.server_ip = self.get_local_ip()
        self.address = (self.server_ip, self.PORT)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.address)
        self.is_logged_in = False
        self.buyer_id = None
        self.show_options()

    @staticmethod
    def get_local_ip():
        # Attempts to open a UDP socket and gets the local IP address
        # The IP address is determined by creating a UDP socket and connecting to an external address
        # (the connection is never actually made, but it allows the socket to determine its own IP)
        try:
            # Attempt to connect to an arbitrary public IP address.
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            print(f"Ip address: {ip}")
            return ip
        except Exception as e:
            print(f"Error: {e}")
            return None

    def send(self, msg):
        # Encodes and sends a message to the server
        # It first sends the length of the message (fixed size, padded with spaces)
        # Then it sends the actual message
        # It waits and receives the server's response, returning it
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)
        server_response = self.client.recv(2048).decode(self.FORMAT)
        return server_response


    def create_account(self, username, password, name):
        # Sends a request to the server to create a new account with the provided details
        create_account_response = self.send(f"CREATE_ACCOUNT {username} {password} {name}")
        print(create_account_response)

    def login(self, username, password):
        # Attempts to log in with the provided username and password
        # If successful, updates the is_logged_in flag and stores the buyer_id
        login_response = self.send(f"LOGIN {username} {password}")
        print(login_response)
        if "Login successful" in login_response:
            self.is_logged_in = True
            buyer_id_response =self.client.recv(2048).decode(self.FORMAT)  
            self.buyer_id = buyer_id_response.split()[-1]
            print(f"Buyer Id: {self.buyer_id}")

    def search_item(self, query):
        # Sends a search query to the server and prints the received search results
        search_results = self.send(f"SEARCH {query}")
        print(f"Search Results:\n{search_results}")

    def add_to_cart(self, product_id, quantity):
        # Sends a request to add a specific quantity of an item to the cart
        server_response = self.send(f"ADD_TO_CART {self.buyer_id} {product_id} {quantity}")
        print(server_response)

    def remove_item_from_cart(self, product_id, quantity):
        # Sends a request to remove a specific quantity of an item from the cart
        server_response = self.send(f"REMOVE_ITEM_FROM_CART {self.buyer_id} {product_id} {quantity}")
        print(server_response)

    def clear_cart(self):
        # Sends a request to clear the cart
        server_response = self.send(f"CLEAR_CART {self.buyer_id}")
        print(server_response)

    def display_cart(self):
        # Requests the current cart's content and displays it
        cart_items = self.send(f"DISPLAY_CART {self.buyer_id}")
        print(cart_items)

    def get_seller_rating(self, seller_id):
        # Requests and displays the rating of a seller
        seller_rating = self.send(f"GET_SELLER_RATING {seller_id}")
        print(f"Seller Rating: {seller_rating}")

    def provide_feedback(self):
        # Provides feedback for a purchased item
        purchased_items = self.send(f"PROVIDE_FEEDBACK {self.buyer_id}")
        if "No purchase was made" in purchased_items or "Failed to retrieve product details" in purchased_items:
            return
        print(purchased_items)

        # get_product_id =self.client.recv(2048).decode(self.FORMAT)  
        # print(f"[Client] {get_product_id}")
        product_id = input("\nPlease enter the product ID for which you want to provide feedback:")
        # print(f"Product Id: {product_id}")
        feedback_response = self.send(product_id)
        if "Feedback already provided" in feedback_response:
            print(feedback_response)
            return

        feedback_type = input(f"{feedback_response}")
        print(f"Feedback Type: {feedback_type}")
        response = self.send(feedback_type)
        print(response)

    def buyer_purchase_history(self):
        # Requests and displays the purchase history
        purchase_history = self.send(f"PURCHASE_HISTORY {self.buyer_id}")
        print(f"Buyer Purchase History: {purchase_history}")

    def logout(self):
        # Logs out the current user and resets the session
        response = self.send(f"LOGOUT {self.buyer_id}")
        if "Logout successful" in response:
            self.is_logged_in = False
        print(response)

    def show_initial_options(self):
        print("Welcome to the Online Marketplace!")
        print("Please select an option:")
        print("1. Create an account")
        print("2. Login")
        print("3. Exit")
    
    def show_logged_in_options(self):
        print("\n")
        print("4. Search for Items")
        print("5. Add an item to cart")
        print("6. Remove an item in cart")
        print("7. Clear Cart")
        print("8. Display Cart")
        print("9. Purchase History")
        print("10. Provide Feedback")
        print("11. Get Seller Rating")
        print("12. Logout")
    
    def show_options(self):   
        while True:
            if not self.is_logged_in:
                self.show_initial_options()
            else:
                self.show_logged_in_options()

            option = input("\nEnter your choice: ")
            self.handle_option(option)

            if option == '3' and not self.is_logged_in: 
                break
    
    def handle_option(self, option):
        if option == '1':
            username = input("Choose your username: ")
            password = input("Choose your password: ")
            name = input("Enter your name: ")
            self.create_account(username, password, name)
        elif option == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            self.login(username, password)
        elif option == '3':
            self.client.close()
        elif option == '4':
            query = input("Enter search query: ")
            self.search_item(query)
        elif option == '5':
            product_id = input("Enter product id: ")
            quantity = input("Enter quantity: ")
            self.add_to_cart(product_id, quantity)
        elif option == '6':
            product_id = input("Enter product id: ")
            quantity = input("Enter quantity: ")
            self.remove_item_from_cart(product_id, quantity)
        elif option == '7':
            self.clear_cart()
        elif option == '8':
            self.display_cart()
        elif option == '9':
            self.buyer_purchase_history()
        elif option == '10':
            self.provide_feedback()
        elif option == '11':
            seller_id = input("Enter seller ID to get rating: ")
            self.get_seller_rating(seller_id)
        elif option == '12':
            self.logout()
        else:
            print("Invalid option, please try again.")
            self.show_options()

if __name__ == "__main__":
    client = BuyerClient()
