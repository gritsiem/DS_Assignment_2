import threading
from buyer_client import BuyerClient


def startClient():
    client = BuyerClient()

def create_thread():
    number_of_buyer_instances = 100
    threads = []
    print(f"Number of buyer instances: {number_of_buyer_instances}")
    for i in range(number_of_buyer_instances):
        thread = threading.Thread(target = startClient)
        thread.start()
        print("Active connections: ", threading.active_count()-1)
        threads.append(thread)

if __name__ == "__main__":
    create_thread()