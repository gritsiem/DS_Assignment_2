import socket
import time
import requests
import os
import json, jsonpickle
from dotenv import load_dotenv

load_dotenv()

class BuyerClient:

    def __init__(self):
        # self.HEADER = 1024
        self.PORT = os.getenv('PORT')
        # self.FORMAT = 'utf-8'
        # self.DISCONNECT_MSG = "!DISCONNECT"
        self.REST = os.getenv('REST')
        # self.server_ip = self.get_local_ip()
        # self.address = (self.server_ip, self.PORT)
        # self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.client.connect(self.address)
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
            # print(f"Ip address: {ip}")
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

    def create_account(self, reqmethod, endpoint, data):
        # Sends a request to the server to create a new account with the provided details
        jsonData = jsonpickle.encode(data)
        if data != None:
            print("Make request")
        url = "http://" + self.REST + ":" + str(self.PORT) + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            responseData = response.json()
            jsonResponse = json.dumps(responseData, indent=4, sort_keys=True)
            print(f"Create_Account resposne:\n{jsonResponse}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text

    def login(self, reqmethod, endpoint, data):
        # Attempts to log in with the provided username and password
        # If successful, updates the is_logged_in flag and stores the buyer_id
        jsonData = jsonpickle.encode(data)
        if data != None:
            print("Make request")
        url = "http://" + self.REST + ":" + str(self.PORT) + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            responseData = response.json()
            jsonResponse = json.dumps(responseData, indent=4, sort_keys=True)
            print(f"Login resposne:\n{jsonResponse}")
            self.is_logged_in = True
            self.buyer_id = responseData['buyer_id']
            print(f"Buyer id: {self.buyer_id}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text

    def search_item(self, reqmethod, endpoint, data):
        # Sends a search query to the server and prints the received search results
        print(f"Data in client: {data}")
        jsonData = jsonpickle.encode(data)
        if data != None:
            print("Make request")
        url = "http://" + self.REST + ":" + self.PORT + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
            print(f"Search Results:\n{jsonResponse}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text

    def add_to_cart(self, reqmethod, endpoint, data):
        # Sends a request to add a specific quantity of an item to the cart
        jsonData = jsonpickle.encode(data)
        url = "http://" + self.REST + ":" + self.PORT + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
            print(f"Add item to cart response:\n{jsonResponse}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text

    def remove_item_from_cart(self, reqmethod, endpoint, data):
        # Sends a request to remove a specific quantity of an item from the cart
        jsonData = jsonpickle.encode(data)
        url = "http://" + self.REST + ":" + self.PORT + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
            print(f"Remove item from cart response:\n{jsonResponse}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text
    
    def clear_cart(self, reqmethod, endpoint, data):
        # Sends a request to clear the cart
        jsonData = jsonpickle.encode(data)
        url = "http://" + self.REST + ":" + self.PORT + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
            print(f"Clear cart response:\n{jsonResponse}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text

    def display_cart(self, reqmethod, endpoint, data):
        # Requests the current cart's content and displays it
        jsonData = jsonpickle.encode(data)
        url = "http://" + self.REST + ":" + self.PORT + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
            print(f"Display cart response:\n{jsonResponse}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text
        
    def get_seller_rating(self, reqmethod, endpoint, data):
        # Requests and displays the rating of a seller
        jsonData = jsonpickle.encode(data)
        url = "http://" + self.REST + ":" + self.PORT + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
            print(f"Seller rating response:\n{jsonResponse}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text

    def provide_feedback(self, reqmethod, endpoint, data):
        # Provides feedback for a purchased item
        jsonData = jsonpickle.encode(data)
        url = "http://" + self.REST + ":" + self.PORT + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
            print(f"Provide feedback response:\n{jsonResponse}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text

    def buyer_purchase_history(self, reqmethod, endpoint, data):
        # Requests and displays the purchase history
        jsonData = jsonpickle.encode(data)
        url = "http://" + self.REST + ":" + self.PORT + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            responseData = response.json()
            jsonResponse = json.dumps(responseData, indent=4, sort_keys=True)
            print(f"Buyer Purchase History response:\n{responseData}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text
    
    def make_purchase(self, reqmethod, endpoint, data):
        # url = "http://soap-service/MakePurchase"
        # headers = {
        #     "Content-Type": "text/xml; charset=utf-8",
        #     "SOAPAction": "http://soap-service-action/MakePurchase"
        # }
        # body = f"""<?xml version="1.0" encoding="utf-8"?>
        # <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        #     <soap:Body>
        #         <VerifyTransaction xmlns="http://your-namespace/">
        #             <userName>{user_name}</userName>
        #             <creditCardNumber>{credit_card_number}</creditCardNumber>
        #         </VerifyTransaction>
        #     </soap:Body>
        # </soap:Envelope>"""
        print(data)
        jsonData = jsonpickle.encode(data)
        url = "http://" + self.REST + ":" + self.PORT + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            responseData = response.json()
            jsonResponse = json.dumps(responseData, indent=4, sort_keys=True)
            print(f"Make Purchase response:\n{responseData}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text

    def logout(self, reqmethod, endpoint, data):
        # Logs out the current user and resets the session
        jsonData = jsonpickle.encode(data)
        url = "http://" + self.REST + ":" + self.PORT + "/" + endpoint
        print(f"URL: {url}")
        response = reqmethod(url, data = jsonData, headers={'Content-type': 'application/json'})
        if response.status_code == 200:
            jsonResponse = json.dumps(response.json(), indent=4, sort_keys=True)
            self.is_logged_in = False
            print(f"Logout response:\n{jsonResponse}")
            return
        else:
            print(f"response code is {response.status_code}, raw response is {response.text}")
            return response.text

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
        print("12. Make Purchase")
        print("13. Logout")
    
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
       
        # self.measure_throughput()
        # self.response_time()
        # self.client.close()
    
    def response_time(self):
        responsetimes = []
        for i in range(10):
            start = time.time()
            self.get_seller_rating(2)
            end = time.time()
            responsetimes.append(end-start)
    
        print("Response time: ",sum(responsetimes)/10)

    def measure_throughput(self):
        # print("Measuring throughput...")
        client_operations = 1000
        total_time = 0

        for _ in range(client_operations):
            start = time.time()
            self.get_seller_rating(2)
            end = time.time()
            total_time += (end - start)

        throughput = client_operations / total_time
        print(f"Throughput: {throughput} operations/second")

    def handle_option(self, option):
        if option == '1':
            username = input("Choose your username: ")
            password = input("Choose your password: ")
            name = input("Enter your name: ")
            data = {'username': username, 'password': password, 'name': name}
            self.create_account(requests.post, 'createaccount', data)
        elif option == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            data = {'username': username, 'password': password}
            self.login(requests.post, 'login', data)
        elif option == '3':
            self.client.close()
        elif option == '4':
            item_category = input("Enter item category: ")
            keywords_input = input("Enter up to 5 keywords, separated by commas: ")
            keywords = "{" + ",".join(keyword.strip() for keyword in keywords_input.split(',')) + "}"
            data = {'item_category': item_category, 'keywords': keywords}
            self.search_item(requests.post, 'search', data)
        elif option == '5':
            product_id = input("Enter product id: ")
            quantity = input("Enter quantity: ")
            data = {'buyer_id': self.buyer_id, 'product_id': product_id, 'quantity': quantity}
            self.add_to_cart(requests.post, 'additem', data)
        elif option == '6':
            product_id = input("Enter product id: ")
            quantity = input("Enter quantity: ")
            data = {'buyer_id': self.buyer_id, 'product_id': product_id, 'quantity': quantity}
            self.remove_item_from_cart(requests.post, 'removeitem', data)
        elif option == '7':
            data = {'buyer_id': self.buyer_id}
            self.clear_cart(requests.post, 'clearcart', data)
        elif option == '8':
            data = {'buyer_id': self.buyer_id}
            self.display_cart(requests.get, 'displaycart', data)
        elif option == '9':
            data = {'buyer_id': self.buyer_id}
            self.buyer_purchase_history(requests.get, 'purchasehistory', data)
        elif option == '10':
            product_id = input("Enter product id: ")
            feedback_type = input("Please enter your feedback \nChoose 1 for Thumbs Up or 2 for Thumbs Down:")
            data = {'buyer_id': self.buyer_id, 'product_id': product_id, 'feedback_type': feedback_type}
            self.provide_feedback(requests.post, 'provide_feedback', data)
        elif option == '11':
            seller_id = input("Enter seller ID to get rating: ")
            data = {'seller_id': seller_id}
            self.get_seller_rating(requests.get, 'sellerrating', data)
        elif option == '12':
            name = input("Enter name: ")
            credit_card_number = input("Enter credit card number: ")
            expiration_date = input("Enter expiration date in MM/DD/YYYY: ")
            data = {'buyer_id': self.buyer_id, 'name': name, 'credit_card_number': credit_card_number, 'expiration_date': expiration_date}
            self.make_purchase(requests.post, 'makepurchase', data)
        elif option == '13':
            data = {'buyer_id': self.buyer_id}
            self.logout(requests.post, 'logout', data)
        else:
            print("Invalid option, please try again.")
            self.show_options()

if __name__ == "__main__":
    client = BuyerClient()
