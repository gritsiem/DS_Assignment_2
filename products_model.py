import sqlite3

# '''INSERT INTO TABLE customers ({ newid }
# )'''
class ProductModel:
    def __init__(self, id, un, pw):
        self.user_id = id
        self.username = un
        self.password = pw
    # def

class ProductInterface:
    def __init__(self):
        self.connection = sqlite3.connect("products.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                "sellerid" TEXT NOT NULL,           
                "name" TEXT NOT NULL,
                "category" INTEGER NOT NULL,
                "condition" TEXT NOT NULL,
                "price" REAL NOT NULL,
                "keywords" TEXT
            )''')
        
        self.table = [ {"id":1, "sellerid":1,"name":"prod1", "category": 1, "keywords":list(["prod","category1"]),"condition":"new", "price":20.00 },\
                       { "id":2, "sellerid":2, "name":"prod2", "category": 2, "keywords":list(["prod","category2"]),  "condition":"new", "price":10.00 }, \
                        {"id":3, "sellerid":1,"name":"prod3", "category": 3, "keywords":list(["prod","category3"]),"condition":"new", "price":30.00 }]
    



    def addProduct(self, sellerid, name, category, condition, price, keywords):
        # newid = uuid.uuid1()
        try:
            print("inserting")
            self.cursor.execute("INSERT INTO products ('sellerid', 'name' , 'category' , 'condition','price','keywords') \
                                VALUES (?,?,?,?,?,?)",(sellerid, name, category, condition, price, keywords))
            self.connection.commit()
            # self.table.append({"id": newid, "username": un,"password":pw})
        except:
            print("exception")
            return -1
        self.id = self.cursor.lastrowid
        return self.cursor.lastrowid
    
    def editProduct(self, prodid, price):
        # newid = uuid.uuid1()
        try:
            self.cursor.execute("UPDATE products SET PRICE = (?) WHERE ID = (? )",(price,prodid))
            self.connection.commit()
            # self.table.append({"id": newid, "username": un,"password":pw})
        except:
            print("exception")
            return -1
        return prodid
    
    def removeProduct(self, prodid):
        # newid = uuid.uuid1()
        try:
            self.cursor.execute("DELETE FROM products WHERE ID = (? )",(prodid))
            self.connection.commit()
            # self.table.append({"id": newid, "username": un,"password":pw})
        except:
            print("exception")
            return -1
        return prodid
    

        
    def getproducts(self, sellerid):
        products = []
        try:
        # print("seller id", sellerid)
            self.cursor.execute("SELECT id, name, category, condition, price FROM products WHERE SELLERID = ?", sellerid)
            products = self.cursor.fetchall()
        # self.connection.commit()
            # self.table.append({"id": newid, "username": un,"password":pw})
        except:
            return []
        return 
    
    def getRatings(self,sellerid):
        try:
        # print("seller id", sellerid)
            self.cursor.execute("SELECT SUM(thumbsup), SUM(thumbsdown) FROM products WHERE SELLERID = ?", sellerid)
            thumbsups, thumbsdowns= self.cursor.fetchone()
        # self.connection.commit()
            # self.table.append({"id": newid, "username": un,"password":pw})
        except:
            return "error!error!erroe!"
        return thumbsups, thumbsdowns



# test = ProductInterface()
# x = test.addProduct(1,"prod1", 1,"new", 20.00, "prod,category1" )
# print(x)