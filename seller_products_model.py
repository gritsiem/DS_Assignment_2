import psycopg2
import os
from dotenv import load_dotenv
import pickle

# '''INSERT INTO TABLE customers ({ newid }
# )'''

load_dotenv()

# class ProductInterface:
#     def __init__(self):
#         pw = os.getenv('PASSWORD')
#         self.connection = psycopg2.connect(f"dbname='products_db' user='postgres' host='localhost' password='{pw}'")
#         self.cursor = self.connection.cursor()

#         self.cursor.execute('''CREATE TABLE IF NOT EXISTS product (
#                 id SERIAL PRIMARY KEY,
#                 item_name VARCHAR(32),
#                 seller_id INTEGER,
#                 item_category INTEGER CHECK (item_category >= 0 AND item_category <= 9),
#                 keywords VARCHAR(8) [],  
#                 condition VARCHAR(10) CHECK (condition IN ('New', 'Used')),
#                 sale_price DECIMAL,
#                 item_quantity INTEGER,
#                 thumbs_ups INTEGER DEFAULT 0,
#                 thumbs_downs INTEGER DEFAULT 0,
#                 CHECK (array_length(keywords, 1) <= 5)
#             );''')


#     def addProduct(self, sellerid, name, category, condition, price, quantity, keywords):
#         # newid = uuid.uuid1()
#         # try:
#         print("inserting")
#         self.cursor.execute("INSERT INTO product(item_name, seller_id, item_category, condition, sale_price, item_quantity, keywords) VALUES \
#                             (%s, %s, %s,%s,%s,%s, %s) returning id",(name, sellerid, category, condition, price, quantity, keywords))
#         self.connection.commit() 
#             # self.table.append({"id": newid, "username": un,"password":pw})
#         # except:
#         #     print("exception")
#         #     return -1
#         self.id = self.cursor.fetchone()[0]
#         return self.id
    
#     def editProduct(self, prodid, price):
#         # newid = uuid.uuid1()
#         try:
#             self.cursor.execute("UPDATE product SET sale_price = %s WHERE id = %s",(price,prodid))
#             self.connection.commit()
#             # self.table.append({"id": newid, "username": un,"password":pw})
#         except:
#             print("exception")
#             return -1
#         return prodid
    
#     def removeProduct(self, prodid):
#         # newid = uuid.uuid1()
#         try:
#             self.cursor.execute("DELETE FROM product WHERE id = %s",(prodid))
#             self.connection.commit()
#             # self.table.append({"id": newid, "username": un,"password":pw})
#         except:
#             print("exception")
#             return -1
#         return prodid
    

        
#     def getProducts(self, sellerid):
#         products = []
#         #try:
#         print("seller id", sellerid)
#         self.cursor.execute("SELECT id, item_name, item_category, condition, sale_price, item_quantity FROM product WHERE seller_id = %s", (sellerid,))
#         products = self.cursor.fetchall()
#         # self.connection.commit()
#             # self.table.append({"id": newid, "username": un,"password":pw})
#         # except:
#         #     return []
#         return products 
    
#     def getRatings(self,sellerid):
#         # try:
#         # print("seller id", sellerid)
#         self.cursor.execute("SELECT SUM(thumbs_ups), SUM(thumbs_downs) FROM product WHERE seller_id = %s", (sellerid,))
#         thumbsups, thumbsdowns= self.cursor.fetchone()
#         # self.connection.commit()
#             # self.table.append({"id": newid, "username": un,"password":pw})
#         # except:
#         #     return "error!error!erroe!"
#         return thumbsups, thumbsdowns
    
#     def close_connection(self):
#         self.connection.close()

class ProductInterface:
    def __init__(self):
        pw = os.getenv('PASSWORD')
        self.connection = psycopg2.connect(f"dbname='products_db' user='postgres' host='localhost' password='{pw}'")
        self.cursor = self.connection.cursor()

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS product (
                id SERIAL PRIMARY KEY,
                item_name VARCHAR(32),
                seller_id INTEGER,
                item_category INTEGER CHECK (item_category >= 0 AND item_category <= 9),
                keywords VARCHAR(8) [],  
                condition VARCHAR(10) CHECK (condition IN ('New', 'Used')),
                sale_price DECIMAL,
                item_quantity INTEGER,
                thumbs_ups INTEGER DEFAULT 0,
                thumbs_downs INTEGER DEFAULT 0,
                CHECK (array_length(keywords, 1) <= 5)
            );''')


    def addProduct(self, sellerid, name, category, condition, price, quantity, keywords):
        # newid = uuid.uuid1()
        # try:
        print("inserting")
        self.cursor.execute("INSERT INTO product(item_name, seller_id, item_category, condition, sale_price, item_quantity, keywords) VALUES \
                            (%s, %s, %s,%s,%s,%s, %s) returning id",(name, sellerid, category, condition, price, quantity, keywords))
        self.connection.commit() 
            # self.table.append({"id": newid, "username": un,"password":pw})
        # except:
        #     print("exception")
        #     return -1
        self.id = self.cursor.fetchone()[0]
        return self.id
    
    def editProduct(self, prodid, price, sellerid):
        # newid = uuid.uuid1()
        try:
            self.cursor.execute("UPDATE product SET sale_price = %s WHERE id = %s AND seller_id= %s",(price,prodid,sellerid))
            self.connection.commit()
            # self.table.append({"id": newid, "username": un,"password":pw})
        except:
            print("exception")
            return -1
        res = self.cursor.rowcount
        if(res == 0):
            return -1
        return prodid
    
    def removeProduct(self, prodid, seller_id):
        # newid = uuid.uuid1()
        try:
            self.cursor.execute("DELETE FROM product WHERE id = %s AND seller_id= %s",(prodid, seller_id))
            self.connection.commit()
            # self.table.append({"id": newid, "username": un,"password":pw})
        except:
            print("exception")
            return -1
        res = self.cursor.rowcount
        if(res == 0):
            return -1
        return prodid
    

        
    def getProducts(self, sellerid):
        products = []
        #try:
        # print("seller id", sellerid)
        self.cursor.execute("SELECT id, item_name, item_category, condition, sale_price, item_quantity FROM product WHERE seller_id = %s", (sellerid,))
        products = self.cursor.fetchall()
        # self.connection.commit()
            # self.table.append({"id": newid, "username": un,"password":pw})
        # except:
        #     return []
        return products 
    
    def getRatings(self,sellerid):
        try:
        # print("seller id", sellerid)
            self.cursor.execute("SELECT SUM(thumbs_ups), SUM(thumbs_downs) FROM product WHERE seller_id = %s", (sellerid,))
            thumbsups, thumbsdowns= self.cursor.fetchone()
            self.connection.commit()
            # self.table.append({"id": newid, "username": un,"password":pw})
        except Exception as e:
            return -1
        return thumbsups, thumbsdowns
    
    def close_connection(self):
        self.connection.close()



# test = ProductInterface()
# x = test.addProduct(1,"prod1", 1,"new", 20.00, "prod,category1" )
# print(x)