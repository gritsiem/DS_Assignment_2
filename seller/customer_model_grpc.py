import customers_pb2_grpc as pb2grpc
import customers_pb2 as pb2

import time
import grpc
import os
from ast import literal_eval


class CustomerInterfaceGRPC:
    def __init__(self):
        '''
        Initializes required parameters for socket connection and also begins communication. 
        '''
        self._PORT = "6080"
        self._SERVER = "localhost"
        self._ADDRESS = self._SERVER+":"+self._PORT
        self.__stub = None
        self.inititate_connection()

    def inititate_connection(self):
        self.channel = grpc.insecure_channel(self._ADDRESS,options=(('grpc.enable_http_proxy',0),))
        self.__stub = pb2grpc.CustomersStub(self.channel)

    def insertCustomer(self, un, pw):
        try:
            insertRequest = pb2.InsertMessage(table_name="seller",  columns ="username,password",values=f"{un},{pw}")
            response = self.__stub.InsertSeller(insertRequest)
        except Exception as e:
            print(e)
            return -1

        # print("last row id",response)
        return response.msg
    
        
    def getUser(self, un, pw=None):
        user = None
        try:
            if pw:

                selectRequest = pb2.SelectManyMessage(table_name="seller", columns ="username,password",search_values=f"{un},{pw}")
                response = self.__stub.GetRowByMultiColumns(selectRequest)
            else:
                selectRequest = pb2.SelectOneMessage(table_name="seller", column ="username",search_value=un)
                response = self.__stub.GetRowsByColumn(selectRequest)
        except Exception as e:
            print(e)
            return -1
        users = literal_eval(response.msg)
        if(len(users)):
            user = users[0]
        return user
    
    def updateFeedback(self, seller_id,tu,td):
        # msg = f"UPDATEBYCOL;seller;thumbs_up_count,thumbs_down_count;{tu},{td};id;{seller_id}"
        updateRequest = pb2.UpdateMessage(table_name="seller", columns ="thumbs_up_count,thumbs_down_count",values=f"{tu},{td}", condition_col="id", condition_val=seller_id)
        response = self.__stub.UpdateRowByColumn(updateRequest)
        # return didUpdate
        return response.msg
    

if __name__ == "__main__":
    client = CustomerInterfaceGRPC()
    print(client.updateFeedback(3,3,4))