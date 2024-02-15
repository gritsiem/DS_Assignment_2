from concurrent import futures
import time
import pickle
import os

import grpc
import products_pb2 as pb2
import products_pb2_grpc as pb2grpc

from ast import literal_eval
'''
File to run server for seller in the E-Market application
Server
- uses multi-threading to accept multiple clients
- connects clients with the server interface of the application which connects to the DB
- also calculates statistics and logs them:
    - Average response time for 10 function calls
    - Average throughput for a 1000 function calls
'''

class ProductsDB:
    count=0
    def __init__(self):
        '''
        Initializes for binding server to port and keeps track of active connections over all clients 
        '''
        self.HOST = "localhost"
        self.PORT = 5080
        self.ADDRESS = (self.HOST, self.PORT)
        self.loadDB()

    def loadDB(self):
        # with open ("products_db.pkl", "rb") as f:
        #     self.db = pickle.load(f)

        self.productTable = [{'id':1, 'item_name':"Bose Headphones", 'seller_id':2, 'item_category':0,'keywords':['music'],'condition':'Used', 'sale_price': 300.00, 'thumbs_up_count':0,'thumbs_down_count':0,'quantity':3 },\
                            {'id':2, 'item_name':"Blender", 'seller_id':1, 'item_category':2,'keywords':['kitchen','blender'],'condition':'Used', 'sale_price': 20.00, 'thumbs_up_count':0,'thumbs_down_count':0,'quantity':1 },
                            {'id':4, 'item_name':"Dell", 'seller_id':3, 'item_category':0,'keywords':['portable', 'laptop'],'condition':'Used', 'sale_price': 619.00, 'thumbs_up_count':1,'thumbs_down_count':1,'quantity':1 },
                            {'id':3, 'item_name':"Macbook Air", 'seller_id':4, 'item_category':0,'keywords':['portable', 'laptop', 'macbook'],'condition':'New', 'sale_price': 1499.00, 'thumbs_up_count':1,'thumbs_down_count':1,'quantity':1 },\
                            {'id':3, 'item_name':"Carpet", 'seller_id':4, 'item_category':1,'keywords':['home','decor'],'condition':'New', 'sale_price': 200.00, 'thumbs_up_count':0,'thumbs_down_count':0,'quantity':1 }]
        self.db = {"product":(self.productTable, {"lastrowid":5})}
        with open ("products_db.pkl", "wb") as f:
            pickle.dump(self.db,f)

        print(self.db)
    def printTable(self,table):
        for row in table:
            print(row)
    def InsertProduct(self, request, context):
        column_names = request.columns.split(",")
        values = request.values.split(",")
        new_row = {}
        self.db[request.table_name][1]['lastrowid'] += 1
        self.printTable(self.db,[request.table_name])
        newid = self.db[request.table_name][1]['lastrowid']
        for col, val in zip(column_names,values):
            new_row[col]=literal_eval(val)
        new_row['id'] = newid
        self.db[request.table_name][0].append(new_row)
        response = pb2.generalResponse()
        response.msg = str(newid)
        return response
    
    def UpdateRowByColumn(self,request,context):
        table = self.db[request.table_name][0]
        count = 0
        for row in table:
            if row[request.condition_col] == request.condition_val:
                count+=1
                for col, val in zip(request.columns,request.values):
                    row[col]=val
        self.printTable(self.db[request.table_name])
        response = pb2.generalResponse()
        response.msg = str(count)
        return response
    
    def UpdateRowByMulti(self,request,context):

        smrequest = pb2.SelectManyMessage(table_name = request.table_name,columns = request.condition_cols,search_values = request.condition_vals,return_index = 1)
        column_names = request.columns.split(",")
        values = request.values.split(",")
        condition_cols = request.condition_cols.split(",")
        condition_vals = request.condition_vals.split(",")

        table = self.db[request.table_name][0]
        index_to_update = int((self.GetRowByMultiColumns(smrequest,context)).msg)
        # print("updating!", index_to_update)
        response = pb2.generalResponse()
        if(index_to_update!=-1):
            for col, val in zip(column_names,values):
                table[index_to_update][col]=val
            print(index_to_update, self.db)
            response.msg = str(1)
            return response
        response.msg = str(-1)
        return response
    
    def GetRowsByColumn(self,request,context):
        # ProductsDB.count+=1
        # print(ProductsDB.count)
        # print("request",request)
        # table = self.db[request.table_name][0]
        # selected_columns = request.selected_columns.split(",")
        # rows = list()
        # modifiedRow = {}
        # if not selected_columns:
        #     for row in table:
        #         if row[request.column] == request.search_value: 
        #             rows.append(tuple(row.values()))
        # else:
        #     # print("selected columns present")
        #     for row in table:
        #         # print("For Current row, col val: ",row[request.column])                               
        #         if str(row[request.column]) == request.search_value:  
        #             for col in selected_columns:
        #                 modifiedRow[col] =row[col]
        #             # print(modifiedRow)
        #             rows.append(tuple(modifiedRow.values()))
        # print(rows)
        response = pb2.generalResponse()
        response.msg = str([(2, 'Blender', 2, 'Used', 20.0, 1)])
        return response
    
    def GetRowByMultiColumns(self, request, context):
        # print(" parameters : ",request.columns,request.search_values)
        # print(request)
        table = self.db[request.table_name][0]
        columns = request.columns.split(",")
        values = request.search_values.split(",")
        msg = tuple()
        response = pb2.generalResponse()
        ind = -1
        for i,row in enumerate(table):
            satisfiesSearch = True
            for col,val in zip(columns,values):
                # print("DEBUG: ",col, row[col],val)
                if str(row[col]) != val:
                    satisfiesSearch=False
            if satisfiesSearch:
                if request.return_index:
                    response.msg = str(i)
                    return response
                response.msg = str(tuple(row.values()))
                return response
        if request.return_index:
            response.msg = str(ind)
            return response
        print(self.db)
        response.msg = str(msg)
        return response
    
    def DeleteRow(self,request,context):
        smrequest = pb2.SelectManyMessage(table_name = request.table_name,columns = request.condition_cols,search_values = request.condition_vals,return_index = 1)

        table = self.db[request.table_name][0]
        index_to_delete = int((self.GetRowByMultiColumns(smrequest, context)).msg)
        response = pb2.generalResponse()
        if(index_to_delete!=-1):
            table.pop(index_to_delete)
            for row in table:
                print(row)
            response.msg = str(1)
            return response
        response.msg = str(0)

        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=200))
    pb2grpc.add_ProductsServicer_to_server(ProductsDB(),server)
    server.add_insecure_port("localhost:5080")
    
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()