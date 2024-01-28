import socket


class Connection:
    def __init__(self):
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

    def send(self):
        msg= input()
        message = msg.encode(self._FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self._FORMAT)
        padded_send = send_length+ b" "*(self._HEADER-len(send_length))
        self.client.send(padded_send)
        self.client.send(message)

    def handleComm(self):
        while True:
            # print("waiting for resp")
            response = self.client.recv(self._RECEIVE).decode(self._FORMAT)
            # print("Got resp")
            print(response)
            # print("sending new input")
            self.send()
    

    


# send("Hello server") 
# send("bye")
# send()
    
conn = Connection()
# print(conn.client.recv(1024).decode("utf-8"))
# print(conn.client.recv(1024).decode("utf-8"))