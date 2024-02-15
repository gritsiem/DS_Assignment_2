'''
Server side interface
- serves options to the client ( menu-system)
- invokes apis to the databases
- parses responses for client

- Three classes:
    - Seller Portal
    provides options to the seller to do various operations.
    Provides one function that distributes the control to the appropriate menu option
    Takes appropriate inputs and calls those functions

    - Seller
    Stores seller login data, and other characteristics like feedback, number of items sold.
    Communicates to the seller table to do the login, registration and validations
'''
import jwt
# from seller_products_model import ProductInterface
# from seller_customer_model import CustomerInterface
from product_model_grpc import ProductInterfaceGRPC
from customer_model_grpc import CustomerInterfaceGRPC
import time


class Seller:
    def __init__(self):
        self._username = None
        self._password = None
        self.id = None
        self._isLoggedIn = False
        self.db = CustomerInterfaceGRPC()
        self.REGISTRATION_ERROR = "Account creation failed, please try again."
        self.USER_EXISTS_ERROR = "Username already exists, please try again."
        self.LOGIN_ERROR = "Login failed, please try again."
        self.itemsSold = 0
    
    def registerUser(self,un,pw):
     
        #contact customer db
        # if there's a customer with that name and password already
        # generate error
        # else
        # add user to the DB

        if not self.db.getUser(un):
            id = self.db.insertCustomer(un, pw)
            user = {'id':id,'un':un}
            token = jwt.encode(user,"secret",algorithm="HS256")
            return 1,{"token":token}
        else:
            return -1, self.USER_EXISTS_ERROR

    def loginUser(self, un, pw):
        
        # Assumes that the usernames are unique ultimately
        # Try to fetch the user using the credentials
        user = self.db.getUser(un,pw)
        print(user)
        # if user exists in the table, log them in
        if user:
            # Also store seller id required for the other options
            user={'id':user[0],'un':user[1]}
            token = jwt.encode(user,"secret",algorithm="HS256")
            return 1, {"token":token}
        else:
            return 2, self.LOGIN_ERROR

        # print("login flow working")
    
    def setUsername(self,un):
        self._username = un

    def setPassword(self,pw):
        self._password = pw

    def getUsername(self):
        return self._username 

    def getPassword(self):
        return self._password 
    
    def validateUser(self,un,pw):
        # validation function for the registration process
        isvalid  = True
        message = ""
        if len(un.strip())==0 or len(un.strip())>32:
            isvalid=False
            message = "Please enter valid username\n"
        if len(pw.strip())<6:
            isvalid=False
            message += "Please enter valid password\n"
        return isvalid, message
    
    def updateFeedback(self, tu, td):
        self.feedback = (tu,td)
        self.db.updateFeedback(self.id,tu,td)

    # def getHash(self,pw):
    #     return hashlib.sha256(pw.encode())

    #Clear seller details in case of logout, or failed authentication
    
    def cleandb(self):
        self.db.close_conn()
        

class Products:
    '''
    Stores the item related information when taking input from user
    provides interface to Products DB
    '''
    def __init__(self):
        self.proddb = ProductInterfaceGRPC()
        self.prodid = None
        self.sellerid = None
        self.name  = None
        self.category  = None
        self.condition = None
        self.price = None
        self.quantity = None
        self.keywords = None
        self.feedback = None
        self.sellerproduts = []

    def getProductsBySeller(self, token):
        '''
        Get all products of a particular seller 
        '''
        decoded_token = jwt.decode(token, options={"verify_signature":False})
        # print("Decoded token: ",decoded_token)
        id = decoded_token["id"]
        products = [] 
        try:
            products = self.proddb.getProducts(id)
        except Exception as e:
            print("there was an error: ", e)
            return -1
        return products
    
    def addProduct(self,token,name,category,condition,price,quantity,keywords):
        decoded_token = jwt.decode(token, options={"verify_signature":False})
        sellerid = decoded_token["id"]
        try:
            self.prodid = self.proddb.addProduct(sellerid,name, category,condition,price,quantity,keywords)
        except Exception as e:
            print("there was an error: ", e)
            return -1
        return self.prodid
    
    def editProduct(self,token,prodid,price):
        decoded_token = jwt.decode(token, options={"verify_signature":False})
        sellerid = decoded_token["id"]
        decoded_token = jwt.decode(token, options={"verify_signature":False})
        sellerid = decoded_token["id"]
        try:
            id = self.proddb.editProduct(prodid,price, sellerid)
            # self.table.append({"id": id, "productname": name,"category":category, "conditon" : condition, "price": price, "keywords": keywords})
        except Exception as e:
            print("there was an error: ",e)
            return -1
        return id
    
    def removeProduct(self,token,prodid):
        decoded_token = jwt.decode(token, options={"verify_signature":False})
        sellerid = decoded_token["id"]
        try:
            id = self.proddb.removeProduct(prodid, sellerid)
            # self.table.append({"id": id, "productname": name,"category":category, "conditon" : condition, "price": price, "keywords": keywords})
        except:
            print("there was an error")
            return -1
        return id
    
    def getRatings(self,token):
        decoded_token = jwt.decode(token, options={"verify_signature":False})
        sellerid = decoded_token["id"]
        self.feedback = self.proddb.getRatings(sellerid)
        return self.feedback
    
    def validateProduct(self):
        '''
        Validate input for 
        '''
        message = ""
        isValid = True
        if len(self.name)>32:
            isValid =  False
            message += "Product name should be at most 32 characters\n"
        
        if int(self.category)<0 or int(self.category)>9:
            isValid = False
            message += "Product category should be an integer between 0 and 9\n"

        if self.condition!="New" and self.condition!="Used":
            isValid = False
            message += "Product condition should be either 'New' or 'Used' \n"

        if not self.price.replace(".","").isnumeric():
            isValid = False
            message += "Price should be a number.\n"

        return isValid, message
    
    def cleandb(self):
        self.proddb.close_conn()

        

class SellerPortal:
    """
    Class to handle a seller's actions in the e-market application.
    """
    def __init__(self):
        self.LOGIN_STATUS = False
        self._global_error = None
        self._WELCOME_MESSAGE = "Welcome to the Seller Portal! Please choose one of the options:\n"
        self._homeMenu = { 1:"Login", 2:"Create Account",  3:"Exit"}
        self._landingMenu = {  1: "Product Catalogue" , 2: "Add a product" , 3: "Edit Product" , 4: "Remove Product" , 5: "See Rating" 
             , 6: "Logout"}
        self.currentMenu = "home"
        self.INCORRECT_INPUT_ERROR = "Incorrect response. Please choose something else."
        self.seller = Seller()
        self.globalResponse= {'msg':"",'invokeTime':None} 
        self.products = Products()
        
        
    def getHomeMenu(self):
        return self._homeMenu
    def getLandingMenu(self):
        return self._landingMenu

    def getMenuMessage(self,menu = "home"):
        msg = ""
        menu = self.getHomeMenu if menu == "home" else self.getLandingMenu 
        for key,val in menu().items():
            msg+= f"{key} - {val}\n"
        return msg
    
    def getWelcomeMessage(self):
        return self._WELCOME_MESSAGE + self.getMenuMessage("home")

    def getProducts(self,token):
        # Set function invocation time
        self.globalResponse["invokeTime"] = time.time()
        # API call
        products=self.products.getProductsBySeller(token)

        productmessage=""

        # Case when no products or an error has occured.
        if(products ==-1):
            productmessage="There was an error. Please try later. "
        if len(products)==0:
            productmessage="You have no products. "

        # Normal case
        for row in products:
            productmessage+=f" #{row[0]} - {row[1]} \n ------------\n Category: {row[2]} \n Condition: {row[3]}\n Price: {row[4]}\n Quantity: {row[5]}\n\n"
        # give control back to main menu function
        self.globalResponse["msg"] = productmessage + "\n" + self.getMenuMessage("landing")

        return self.globalResponse
    
    def handleAddProduct(self, token, name, category,condition,price,quantity,keywords):
        
        # valid, msg = self.products.validateProduct()

        # if not valid:
        #     self.globalResponse["msg"] = msg + "\nPlease try again. \n\nPress enter to get back to the main menu"
        #     return self.globalResponse
        
        keywords = keywords.split(',')
        newid = self.products.addProduct(token,name, category,condition,price,quantity,keywords)
        self.globalResponse["msg"] = "Product added successfully!\n\nPress enter to get back to the main menu"
        self.currentPage = 0
        return self.globalResponse
        

    def handleEditProduct(self, token,prodid,price):

        updated = self.products.editProduct(token,prodid,price)
        if updated == -1:
            self.globalResponse["msg"] = "The ID is incorrect. Please give a valid product ID. \n\nPress enter to get back to the main menu"
        else:
            self.globalResponse["msg"] = "Product edited successfully!\n\nPress enter to get back to the main menu"
        self.currentPage = 0
        return self.globalResponse

    def handleRemoveProduct(self, token,prodid):
        updated = self.products.removeProduct(token,prodid)
        print(updated)
        if updated == -1:
            self.globalResponse["msg"] = "The ID is incorrect. Please give a valid product ID. \n\nPress enter to get back to the main menu"
        else:
            self.globalResponse["msg"] = "Product removed successfully!\n\nPress enter to get back to the main menu"
        self.currentPage = 0
        return self.globalResponse
    
    def handleGetRatings(self,token):
        # No input needed
        # call api
        feedback = self.products.getRatings(token)

        #update seller feedback
        self.seller.updateFeedback(*feedback)
        # Give response to user
        self.globalResponse["msg"] = f"Your feedback is: \n Thumbs Ups: {feedback[0]} Thumbs Downs: {feedback[1]} \n\n Please press enter to go back to the menu"
        self.currentPage=0
        return self.globalResponse

    def handleLogin(self, un,pw):

        self.globalResponse["invokeTime"] = time.time()
        
        # if not self.seller.validateUser(self._username,self._password):
        #     self.globalResponse["msg"] = "Please enter valid username and password"
        #     return self.globalResponse
        
        code, msg = self.seller.loginUser(un,pw)
        if  code == 1:
            self.globalResponse["msg"] = f"Logged in for {un}\n"+self.getMenuMessage(menu="landing")
            self.globalResponse["data"] = msg
        else:
            self.globalResponse["msg"] = msg + "\nPlease try again"+ self.getMenuMessage("home")

        return self.globalResponse

    def handleRegistration(self, un,pw):
        
        isValid, errmsg = self.seller.validateUser(un,pw)
        if not isValid:
            self.globalResponse["msg"] = errmsg
            self.currentPage = 0
            return self.globalResponse

        # call api
        code, msg = self.seller.registerUser(un,pw)

        # generate response based on api result
        if  code == 1:
            self.globalResponse["msg"] = f"Created Account for {un} \nPress enter to go to the landing menu"
            self.globalResponse["data"] = msg
        else:
            self.globalResponse["msg"] = msg + "Please try again.\n" + self.getMenuMessage("home")
            self.globalResponse["data"] = ""
        return self.globalResponse   

    def handleLogout(self, inactivity = False):
        self.LOGIN_STATUS = False
        # if inactivity:
        #     self.currentPage=0
        #     return {"msg": "You were logged out because of inactivity. Please login again.\n\n" + self.getMenuMessage("home"), "invokeTime":None}
        self.globalResponse["msg"] = "Logging out...\n\n" + self.getMenuMessage("home")
        self.globalResponse["invokeTime"] = None
        self.products.cleandb()

        
    def handleExit(self):
        self.products.cleandb()
        self.seller.cleandb()
        self.globalResponse["msg"] = "!DISCONNECT"
        self.globalResponse["invokeTime"] = None
    
    def handleBadResponse(self):
        self.globalResponse["msg"] = self.INCORRECT_INPUT_ERROR
        self.globalResponse["invokeTime"] = None
