import threading
from seller_client import Client
import time


counter = 0
def startClient():
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

    client = Client()
    client.login()
    for i in range(1000):
        start =time.time() 
        client.getProducts()
        end = time.time()
        # if a function is invoked, and there is a valid run for stats
                # (10 for response time and 1000 for throughput)
        if responseCounter<11:    
            # log the next response time for current run
            responseTimes.append(end-start)

            # add operation time to total time for throughput calculation
            optimes+= end-start

            # update run counters
            responseCounter+=1
            tpcounter+=1

            # end of run calculation for both stats
            # reset counters for the next run
            if tpcounter == 99:
                stats["atp"].append((tpcounter-1)/optimes)
                tpcounter=0
                optimes = 0

            if responseCounter==11:
                # stats["art"].append(sum(responseTimes)/10)
                stats["art"].append(sum(responseTimes)/10)
                responseTimes = []
                responseCounter=0
    client.logout()
    with open("log.txt", "a") as f:
        f.write(f"Average Response times for client :  {stats['art']} \n")
        f.write(f"Average throughput for client :  {stats['atp']} \n========\n")

for i in range(100):
    # time.sleep(0.5)
    print(i)
    thread = threading.Thread(target = startClient)
    thread.start()

