import psycopg2
import os
from dotenv import load_dotenv

# '''INSERT INTO TABLE customers ({ newid }
# )'''

load_dotenv()

class CustomerInterface:
    def __init__(self):
        pw = os.getenv('PASSWORD')
        self.connection = psycopg2.connect(f"dbname='customers_db' user='postgres' host='localhost' password='{pw}'")
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS seller (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(32) NOT NULL,
                    password VARCHAR(12) CHECK(char_length(password) BETWEEN 6 and 12),
                    thumbs_up_count INTEGER DEFAULT 0,
                    thumbs_down_count INTEGER DEFAULT 0,
                    items_sold INTEGER DEFAULT 0
                );''')
        except Exception as e:
            print("creation error", e)
        self.connection.commit()
        # self.table = [{"id": "12", "username": "user12","password":"12"}, \
        #               {"id": "1", "username": "user1","password":"one"}]



    def insertCustomer(self, un, pw):
        try:
            self.cursor.execute("INSERT INTO seller (username, password) VALUES \
                    (%s, %s) returning id",(un, pw))
            newid = self.cursor.fetchone()[0]
        except Exception as e:
            print(e)
            return -1

        print("last row id",newid)
        self.connection.commit() 
        return newid
    
        
    def getUser(self, un, pw=None):
        user = None
        try:
            # self.cursor.execute("INSERT INTO ")
            # self.table.append({"id": newid, "username": un,"password":pw})
            if pw:
                self.cursor.execute("SELECT id, username, password FROM seller WHERE username = %s AND password = %s",(un, pw))
                user = self.cursor.fetchone()
            else:
                self.cursor.execute("SELECT id, username, password FROM seller WHERE username = %s",(un))
                user = self.cursor.fetchone()
                
        except Exception as e:
            print(e)
            return -1
        return user
        

        # for row in self.table:
        #     # print("Current row ==>", row, row["username"], row["password"])
        #     if row["username"]== un and  row["password"] == pw:
        #         return row
        # return None
    
    def updateFeedback(self, seller_id,tu,td):
        self.cursor.execute("UPDATE seller SET thumbs_up_count = %s, thumbs_down_count = %s WHERE id = %s",(tu,td, seller_id))
        self.connection.commit()
        return 1




