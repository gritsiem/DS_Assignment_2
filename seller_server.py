import socket
import threading
from seller import SellerPortal

class Server:
    def __init__(self):
        self.HEADER = 64
        SERVER = socket.gethostbyname(socket.gethostname())
        self.PORT = 6050
        self.ADDRESS = (SERVER, self.PORT)
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "bye"
        self.active_connections = 0

    def initialize_server(self):
        self.server = socket.socket(family=socket.AF_INET, type = socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)
        print(f"Starting server at {self.PORT}...")

    
    def start_server(self):
        self.server.listen()
        while True:
            connection, address = self.server.accept()
            thread = threading.Thread(target = self.handleClient, args=(connection, address))
            thread.start()
            self.active_connections = threading.active_count()-1
            print("Active connections ", self.active_connections)

    def handleClient(self,client, address):
        print("New Connection: ", address)
        connected = True
        seller = SellerPortal()
        self.send(client,seller.getWelcomeMessage())
        while connected:
            msg_len = client.recv(self.HEADER).decode(self.FORMAT) # blocking
            if msg_len:
                msg_len = int(msg_len)
                msg = client.recv(msg_len).decode(self.FORMAT) 
                response = seller.getResponse(msg)
                print(response)
                if(response == "!DISCONNECT"):
                    connected  = False
                else:
                    self.send(client,response)
               
                # print(f"[{address}] says: {msg}")
        client.close()

    def send(self,client, msg):
        print(msg, type(msg))
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        # send_length = str(msg_length).encode(self.FORMAT)
        # print("message length 32 ", )
        padded_message = message + b" " * (self.HEADER-msg_length)
        # Header plus message
        # client.send(padded_send)
        client.send(padded_message)
        

server = Server()
server.initialize_server()
server.start_server()