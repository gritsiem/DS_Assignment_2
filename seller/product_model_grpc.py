import products_pb2_grpc as pb2grpc
import products_pb2 as pb2

import time
import grpc
import os
from ast import literal_eval


class ProductInterfaceGRPC:
    counter = 0
    def __init__(self):
        '''
        Initializes required parameters for socket connection and also begins communication. 
        '''
        self._PORT = "5080"
        self._SERVER = "localhost"
        self._ADDRESS = self._SERVER+":"+self._PORT
        self.__stub = None
        self.inititate_connection()

    def inititate_connection(self):
        self.channel = grpc.insecure_channel(self._ADDRESS,options=(('grpc.enable_http_proxy',0),))
        self.__stub = pb2grpc.ProductsStub(self.channel)
        ProductInterfaceGRPC.counter+=1
        print(ProductInterfaceGRPC.counter)

    def addProduct(self, sellerid, name, category, condition, price, quantity, keywords):

        print("inserting")
        insertRequest = pb2.InsertMessage(table_name="product",  columns ="item_name,seller_id,item_category,condition,sale_price,quantity,keywords",values=f"{name},{sellerid},{category},{condition},{price},{quantity},{keywords}")
        response = self.__stub.InsertProduct(insertRequest)
        return response.msg
    
    def editProduct(self, prodid, price, sellerid):
        try:
            updateRequest = pb2.UpdateManyMessage(table_name="product",  columns ="sale_price",values=f"{price}", condition_cols = "id,seller_id", condition_vals=f"{prodid},{sellerid}")
            response = self.__stub.UpdateRowByMulti(updateRequest)     
        except Exception as e:
            print("exception", e)
            return -1
        
        if(response.msg == "-1"):
            return -1
        return response.msg
    
    def removeProduct(self, prodid, seller_id):
        # newid = uuid.uuid1()
        try:
            deleteRequest = pb2.DeleteMessage(table_name="product", condition_cols = "id,seller_id", condition_vals=f"{prodid},{seller_id}")
            response = self.__stub.DeleteRow(deleteRequest)     
            print("ID: ",response)
            # self.table.append({"id": newid, "username": un,"password":pw})
        except:
            print("exception")
            return -1
        if int(response.msg) == 0:
            return -1
        return prodid
    

        
    def getProducts(self, sellerid):
        # print(ProductInterfaceGRPC.counter)
        products = []
        #try:
        msg = f""
        selectRequest = pb2.SelectOneMessage(table_name="product",  column ="seller_id", search_value=f"{sellerid}", selected_columns = "id,item_name,item_category,condition,sale_price,quantity")
        products = self.__stub.GetRowsByColumn(selectRequest)     
        # Fetch all
        # print("whoop ",products.msg)
        products = literal_eval(products.msg)
        return products 
    
    def getRatings(self,sellerid):
        try:
            # print("seller id", sellerid)
            selectRequest = pb2.SelectOneMessage(table_name="product",  column ="seller_id", search_value=f"{sellerid}", selected_columns = "thumbs_up_count,thumbs_down_count")
            response = self.__stub.GetRowsByColumn(selectRequest)     
            # Fetch all
            feedbacks = response.msg
        except Exception as e:
            print(e)
            return -1
        feedbacks = literal_eval(feedbacks)
        thumbsups = 0
        thumbsdowns = 0
        for feedback in feedbacks:
            thumbsups+=feedback[0]
            thumbsdowns += feedback[1]
        return thumbsups, thumbsdowns
    def close_conn(self):
        # self.channel.close()
        pass

if __name__ == "__main__":
    client = ProductInterfaceGRPC()
    # print(client.addProduct(2, "randomproduct", 9, 1, 100.00, 3, "['random']"))
    # print(client.getProducts(1))
    # print(client.getRatings(3))
    # print(client.editProduct(2,25.00,1))
    print(client.removeProduct(2,1))