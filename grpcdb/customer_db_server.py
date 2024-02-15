from concurrent import futures
import time
import pickle
import os

import grpc
import customers_pb2 as pb2
import customers_pb2_grpc as pb2grpc

'''
File to run server for seller in the E-Market application
Server
- uses multi-threading to accept multiple clients
- connects clients with the server interface of the application which connects to the DB
- also calculates statistics and logs them:
    - Average response time for 10 function calls
    - Average throughput for a 1000 function calls
'''

class CustomerDB(pb2grpc.CustomersServicer):
    def __init__(self):
        '''
        Initializes for binding server to port and keeps track of active connections over all clients 
        '''
        self.HOST = "localhost"
        self.PORT = 6080
        self.ADDRESS = (self.HOST, self.PORT)
        self.loadDB()

    def loadDB(self):
        # with open ("customers_db.pkl", "rb") as f:
        #     self.db = pickle.load(f)

        self.sellerTable = [{'id':1, 'username':"user1", 'password':'userone','thumbs_up_count':0,'thumbs_down_count':0,'items_sold':0 },\
                            {'id':2, 'username':"user2", 'password':'usertwo','thumbs_up_count':0,'thumbs_down_count':0,'items_sold':0 },
                            {'id':4, 'username':"user4", 'password':'userfour','thumbs_up_count':0,'thumbs_down_count':0,'items_sold':0 },
                            {'id':3, 'username':"user3", 'password':'userthree','thumbs_up_count':1,'thumbs_down_count':1,'items_sold':0 }]
        self.db = {"seller":(self.sellerTable, {"lastrowid":4})}
        with open ("customers_db.pkl", "wb") as f:
            pickle.dump(self.db,f)

        print(self.db)
        # self.db["buyer"] = (,{lastrow})
    
    def InsertSeller(self,request,context):
        columns = request.columns.split(",")
        values = request.values.split(",")
        new_row = {}
        newid = self.db[request.table_name][1]['lastrowid'] + 1
        self.db[request.table_name][1]['lastrowid']+=1
        # print("DEBUG: ",newid)
        for col, val in zip(columns,values):
            new_row[col]=val
        new_row['id'] = newid
        # print("DEBUG2: ",new_row)
        self.db[request.table_name][0].append(new_row)
        print(self.db)

        response = pb2.generalResponse()
        response.msg = str(newid)
        return response
    
    def UpdateRowByColumn(self,request,context):
        columns = request.columns.split(",")
        values = request.values.split(",")
        condition_col = request.condition_col
        condition_val = request.condition_val
        
        updated = 0
        table = self.db[request.table_name][0]
        for row in table:
            if row[condition_col] == condition_val:
                for col, val in zip(columns,values):
                    row[col]=val
                    updated+=1
        response = pb2.generalResponse()
        response.msg = str(updated)
        return response
    
    def GetRowsByColumn(self, request, context):
        #,table_name, column , search_value
        table = self.db[request.table_name][0]

        rows = list()  
        response = pb2.generalResponse()    
        for row in table:
            if row[request.column] == request.search_value: 
                rows.append(tuple(row.values()))
        response.msg = str(rows)
        return response
    
    def GetRowByMultiColumns(self, request,context):
        #,table_name, columns , search_values,return_index=False
        columns = request.columns.split(",")
        search_values = request.search_values.split(",")
        table = self.db[request.table_name][0]
        rows = list()
        response = pb2.generalResponse()
        for i,row in enumerate(table):
            satisfiesSearch = True
            for col,val in zip(columns,search_values):
                if row[col] != val:
                    satisfiesSearch=False
            if satisfiesSearch:
                rows.append(tuple(row.values()))  
        response.msg = str(rows)
        return response
        
        


        

# customerDB = CustomerDB()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=200))
    pb2grpc.add_CustomersServicer_to_server(CustomerDB(),server)
    server.add_insecure_port("localhost:6080")
    
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()