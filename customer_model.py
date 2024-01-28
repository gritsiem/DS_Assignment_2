import sqlite3
import uuid



# '''INSERT INTO TABLE customers ({ newid }
# )'''
class CustomerModel:
    def __init__(self, id, un, pw):
        self.user_id = id
        self.username = un
        self.password = pw
    # def

class CustomerInterface:
    def __init__(self):
        # self.connection = sqlite3.connect("customers.db")
        # self.cursor = self.connection.cursor()
        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS seller (
        #         "id" PRIMARY KEY,
        #         "username" TEXT NOT NULL,
        #         "password" TEXT,
        #         "feedback
        #     )''')
        self.table = [{"id": "12", "username": "user12","password":"12"}, \
                      {"id": "1", "username": "user1","password":"one"}]
        # self.insertCustomer("user1", "pw1")
        # self.insertCustomer("user2", "pw2")
        # self.insertCustomer("user3", "pw3")



    def insertCustomer(self, un, pw):
        newid = uuid.uuid1()
        try:
            # self.cursor.execute("INSERT INTO ")
            self.table.append({"id": newid, "username": un,"password":pw})
        except:
            return -1
        return newid
    
        
    def getUser(self, un, pw):
        for row in self.table:
            # print("Current row ==>", row, row["username"], row["password"])
            if row["username"]== un and  row["password"] == pw:
                return row
        return None


