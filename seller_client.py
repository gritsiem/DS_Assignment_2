'''
Client side of the seller functionality of the E-Market application
Client can 
- start connection to the seller server.
- receive messages from the server
- send messages to server
- Additionally an option to generate client side inputs automatically / use actual user input
'''

import socket
import time
from random import randint


class Connection:
    def __init__(self):
        '''
        Initializes required parameters for socket connection and also begins communication. 
        '''
        self._HEADER = 64
        self._SERVER = socket.gethostbyname(socket.gethostname())
        self._PORT = 6050
        self._ADDRESS = (self._SERVER, self._PORT)
        self._FORMAT = "utf-8"
        self.DISCONNECT_MSG = "bye"
        self._RECEIVE = 1024
        self.inititate_connection()

    def inititate_connection(self):
        self.client = socket.socket(family=socket.AF_INET, type = socket.SOCK_STREAM)
        self.client.connect(self._ADDRESS)
        self.handleComm()
    
    def inputScript(self):
        '''
        A very simple input script generator for evaluation
        - user logs in and keeps fetching their listed products
        - logout and then exit to close connection 
        '''
        script = ["1", "user1","userone"]
        script = script + ["1"]*1000 + ["6", "3"]
        l = len(script)
        i=0
        while i < l:
            yield script[i]
            i+=1

    def send(self, msgGenerator):
        '''
        Conducts one send cycle - requires two messages to be sent
        '''

        # either use actual console input or automatic script
        msg= input()
        # msg = next(msgGenerator) 

        # As number of bytes have to be known to receive message in python, client 
        # first sends the length of the message in bytes and then the actual message   
        message = msg.encode(self._FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self._FORMAT)
        padded_send = send_length+ b" "*(self._HEADER-len(send_length))
        self.client.send(padded_send)
        self.client.send(message)

    def handleComm(self):

        '''
        Conducts one cycle of message receieve and send with the server
        '''
    
        msgGenerator = self.inputScript()
        
        while True:
            response = self.client.recv(self._RECEIVE).decode(self._FORMAT)
            # time.sleep(randint(2,5))

            # Detect closed connection when nothing is received from the server
            if(len(response)==0):
                print("Closed connection...")
                return
            # currently commented out for automation purposes. 
            print(response)
            self.send(msgGenerator)
    
# when running from console
if __name__ == "__main__":
    conn = Connection()