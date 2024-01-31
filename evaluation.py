import threading
from seller_client import Connection


def startClient():
    conn = Connection()

for i in range(1):
    thread = threading.Thread(target = startClient)
    thread.start()

