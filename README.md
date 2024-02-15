# CSCI-5673-Distributed-Systems

## Technology stack
- python: libraries Flask, threading, time, grpc
- DB : PostgreSQL
- Cloudlab - for setting up the network
## System Design

1. ### 6 components

1 server and 1 client for role 'Seller', 1 server and client for role 'Buyer'. 1 Products DB and 1 Customers DB. They are moved to the cloud, and just need to provide their different IP addresses and port numbers for clients to be able to access them.

2. ### Database description and gRPC

Customers and Products DB for this assignment is connected using gRPC. There are two proto files to define the prototypes for the customer and products DB respectively. The generated pb2 and pb2_grpc files are shared with the clients as well. All these files can be found in the 'grpcdb' folder. These are the files which will be deployed in the DB server node in the cloud. 

3. ### Buyer class
The server handles all the necessory functions. The client send the request to the server and the server performs operations based on the requests made by the client. The server interacts with db classes to fetch neccesary details from the databases. The server also validates all the requests. The db interface classes 'CustomersDatabase' and 'ProductsDatabase' handles all the incoming db requests and performs required operations in the databases. 

4. ### Seller side interface

Flask is used to create a restful API service which provides the available functions to the clients. The SellerPortal object continues to be used as the. This object uses two more objects ('Seller' and 'Products') to register and validate inputs, while also communicating with the DB Interface classes.

Two DB interface classes (customerInterface_grpc and productInterface_grpc) now act as clients for gRPC server. They subscribe to the channel and use the stub files mentioned in point 2 to query the database.

5. ### Evaluation

The times for calculating Average Server throughput and Average Response Times are only measured for API function calls, (and not when gathering input). To calculate for multiple clients, averages of all values over different clients has been reported. ( Detailed logs available in the seller folder)

## Assumptions

Seller - The Assignment 1 assumptions still hold. The REST requests do not save any state. This means there is no session maintainence and each request is considered separately. The login is handled using a jwt token, which gets stored on the client side and sent for each subsequent request to prove login status.

Buyer -Same as seller login is doneassuming unique usernames. And in a session, some information is persisted in the server. 

Evaluation - The evaluation is carried out only using read functions (fetching products or cart items).


# What doesn't work
There are a few edge cases that are not handled. The seller can upload same product multiple times with all details same as long as ID is autoincremented. Ideally, the quantity should be increased. But similar edge case for adding an item to the cart is handled. In Buyer, one edge case where the number of specific products should be less than or equal to the quantiy of the product is not handled. 
