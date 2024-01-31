'''
File to run server for seller in the E-Market application
Server
- uses multi-threading to accept multiple clients
- connects clients with the server interface of the application which connects to the DB
- also calculates statistics and logs them:
    - Average response time for 10 function calls
    - Average throughput for a 1000 function calls
'''
import socket
import threading
import time
import pickle
from seller import SellerPortal

class Server:
    def __init__(self):
        '''
        Initializes for binding server to port and keeps track of active connections over all clients 
        '''
        self.HEADER = 64
        SERVER = socket.gethostbyname(socket.gethostname())
        self.PORT = 6050
        self.ADDRESS = (SERVER, self.PORT)
        self.FORMAT = "utf-8"
        self.DISCONNECT_MSG = "!DISCONNECT"
        self.active_connections = 0


    def initialize_server(self):
        '''
        Binds the server to the port
        '''
        self.server = socket.socket(family=socket.AF_INET, type = socket.SOCK_STREAM)
        self.server.bind(self.ADDRESS)
        print(f"Starting server at {self.PORT}...")

    
    def start_server(self):
        '''
        Listens to port and creates threads for incoming clients. Also updates the active threads.
        '''
        self.server.listen()
        while True:
            connection, address = self.server.accept()
            thread = threading.Thread(target = self.handleClient, args=(connection, address))
            thread.start()
            self.active_connections = threading.active_count()-1
            print("Active connections ", self.active_connections)

    def handleClient(self,client, address):
        '''
        The entry point for each client.
        - receive messages from the client
        - send appropriate response
        - calculates the stats
        '''

        print("New Connection: ", address)

        # object to log in the file
        stats = {"art":[], "atp":[]} 
        # keep track of response times in 1 run ( 10 operations)
        responseTimes = []
        # how many operations have occcured 
        responseCounter = 0 
        # variable to count operations for throughput calculation in 1 run (1000 operations)
        tpcounter = 0 
        # Sum the total time in 1 run for throughput calculations
        optimes = 0 
        # keep track of connection to stop threa
        connected = True 

        # initialize interface and send first message
        seller = SellerPortal() 
        self.send(client,seller.getWelcomeMessage())

        inactivityTimer = time.time()

        # run loop until client indicates exit
        while connected:

            # Get string from bytes received by client 
            # first part of message - length of the actual message
            if(time.time() - inactivityTimer>=300):
                seller.handleLogout()
            msg_len = client.recv(self.HEADER).decode(self.FORMAT) # blocking
            inactivityTimer = time.time()
            # if message is empty, ignore
            if msg_len:
                msg_len = int(msg_len)

                # second part of message - the content of client input
                msg = client.recv(msg_len).decode(self.FORMAT) 

                # pass the message directly to the interface, get response
                # response has 2 parts - msg and invokeTime (stats)
                response = seller.getResponse(msg)

                # if client exits, detect via disconnect messaget
                if(response["msg"] == self.DISCONNECT_MSG):
                    # stop connection
                    connected  = False
                else:
                    # Continue to send the response message to client
                    self.send(client,response["msg"])
                
                # get post completion time
                end = time.time()

                # if a function is invoked, and there is a valid run for stats
                # (10 for response time and 1000 for throughput)
                if response["invokeTime"] and responseCounter<11:    
                    # log the next response time for current run
                    responseTimes.append(end-response["invokeTime"])

                    # add operation time to total time for throughput calculation
                    optimes+= end - response["invokeTime"]

                    # update run counters
                    responseCounter+=1
                    tpcounter+=1

                    # end of run calculation for both stats
                    # reset counters for the next run
                    if tpcounter == 1001:
                        stats["atp"].append(tpcounter-1/optimes)
                        tpcounter=0
                        optimes = 0

                    if responseCounter ==11:
                        stats["art"].append(sum(responseTimes)/10)
                        responseTimes = []
                        responseCounter=0
               
        
        client.close()

        # log the stats in a file
        with open("log.txt", "a") as f:
            f.write(f"Average Response times for client [{address}]:  {stats['art']} \n")
            f.write(f"Average throughput for client [{address}]:  {stats['atp']} \n========\n")

    # in this case did not send message length and just gave a big enough number for server response
    def send(self,client, msg):
        # print(msg, type(msg))
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        # send_length = str(msg_length).encode(self.FORMAT)
        padded_message = message + b" " * (self.HEADER-msg_length)
        # Header plus message
        # client.send(padded_send)
        client.send(padded_message)
        

server = Server()
server.initialize_server()
server.start_server()