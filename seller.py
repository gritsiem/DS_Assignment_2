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
from seller_customer_model import CustomerInterface
from seller_products_model import ProductInterface
import time


class Seller:
    def __init__(self):
        self._username = None
        self._password = None
        self.id = None
        self._isLoggedIn = False
        self.db = CustomerInterface()
        self.REGISTRATION_ERROR = "Account creation failed, please try again."
        self.USER_EXISTS_ERROR = "Username already exists, please try again."
        self.LOGIN_ERROR = "Login failed, please try again."
        self.itemsSold = 0
    
    def registerUser(self):
     
        #contact customer db
        # if there's a customer with that name and password already
        # generate error
        # else
        # add user to the DB

        if not self.db.getUser(self._username):
            self.id = self.db.insertCustomer(self._username, self._password)
            self._isLoggedIn = True
            return 1,"Success"
        else:
            return -1, self.USER_EXISTS_ERROR

    def loginUser(self, un, pw):
        
        # Assumes that the usernames are unique ultimately
        # Try to fetch the user using the credentials
        user = self.db.getUser(self._username, self._password)
        
        # if user exists in the table, log them in
        if user:
            self._username == user[1]
            # Also store seller id required for the other options
            self.id = user[0]
            self._isLoggedIn = True
            return 1,"Success"
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
    
    def validateUser(self):
        # validation function for the registration process
        isvalid  = True
        message = ""
        if len(self._username.strip())==0 or len(self._username.strip())>32:
            isvalid=False
            message = "Please enter valid username\n"
            self.clearUser()
        if len(self._password.strip())<6:
            isvalid=False
            message += "Please enter valid password\n"
            self.clearUser()
        return isvalid, message
    
    def updateFeedback(self, tu, td):
        self.feedback = (tu,td)
        self.db.updateFeedback(self.id,tu,td)

    # def getHash(self,pw):
    #     return hashlib.sha256(pw.encode())

    #Clear seller details in case of logout, or failed authentication
    def clearUser(self):
        self._username = None
        self._password = None
    
    def cleandb(self):
        self.db.close_conn()
        

class Products:
    '''
    Stores the item related information when taking input from user
    provides interface to Products DB
    '''
    def __init__(self):
        self.proddb = ProductInterface()
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

    def getProductsBySeller(self, sellerid):
        '''
        Get all products of a particular seller 
        '''
        products = [] 
        try:
            products = self.proddb.getProducts(sellerid)
        except Exception as e:
            print("there was an error: ", e)
            return -1
        self.clearProduct()
        return products
    
    def addProduct(self):
        try:
            self.prodid = self.proddb.addProduct(self.sellerid,self.name,self.category, self.condition, self.price, self.quantity, self.keywords)
        except Exception as e:
            print("there was an error: ", e)
            return -1
        self.clearProduct()
        return self.prodid
    
    def editProduct(self):
        try:
            id = self.proddb.editProduct(self.prodid,self.price, self.sellerid)
            # self.table.append({"id": id, "productname": name,"category":category, "conditon" : condition, "price": price, "keywords": keywords})
        except Exception as e:
            print("there was an error: ",e)
            return -1
        self.clearProduct()
        return id
    
    def removeProduct(self):
        try:
            id = self.proddb.removeProduct(self.prodid, self.sellerid)
            # self.table.append({"id": id, "productname": name,"category":category, "conditon" : condition, "price": price, "keywords": keywords})
        except:
            print("there was an error")
            return -1
        self.clearProduct()
        return id
    
    def getRatings(self):
        self.feedback = self.proddb.getRatings(self.sellerid)
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
    
    def clearProduct(self):
        '''
        Reset data for next operation
        '''
        self.prodid = None
        self.sellerid = None
        self.name  = None
        self.category  = None
        self.condition = None
        self.price = None
        self.quantity = None
        self.keywords = None
        self.feedback = None
    
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
        self.pages={0:self.handleNavigation, 1: self.handleLogin, 2: self.handleRegistration, 3: self.getProducts, 4:self.handleAddProduct, 5: self.handleEditProduct, 6:self.handleRemoveProduct, 7:self.handleGetRatings}
        self.currentPage = 0
        self.INCORRECT_INPUT_ERROR = "Incorrect response. Please choose something else."
        self.seller = Seller()
        self.products = Products()
        self.globalResponse = {'msg':"",'time':None} 
        
        
    def getHomeMenu(self):
        return self._homeMenu
    def getLandingMenu(self):
        return self._landingMenu

    def getMenuMessage(self,menu):
        msg = ""
        menu = self.getHomeMenu if menu == "home" else self.getLandingMenu 
        for key,val in menu().items():
            msg+= f"{key} - {val}\n"
        return msg
    
    def getWelcomeMessage(self):
        return self._WELCOME_MESSAGE + self.getMenuMessage("home")


    def handleNavigation(self, selection):
        self.globalResponse["invokeTime"] = None
        if len(selection) == 0:
            self.globalResponse["msg"] = self.getMenuMessage(self.currentMenu)
            return self.globalResponse
        selection = int(selection)
        
        if not self.LOGIN_STATUS:
            if(selection == 1):
                self.currentPage=1
                return self.handleLogin()
            elif (selection==2):
                self.currentPage=2
                return self.handleRegistration()
            elif (selection == 3):
                self.handleExit()
            else:
                self.handleBadResponse()
        else:
            # 1. Product Catalogue 2. Add a product 3. Edit Product 4. Remove Product 5. See Rating 
            # 6. Logout
            if(selection == 1):
                self.currentPage = 3
                return self.getProducts()
            elif (selection == 2):
                self.currentPage = 4
                return self.handleAddProduct()
            elif selection == 3:
                self.currentPage = 5
                return self.handleEditProduct()
            elif selection == 4:
                self.currentPage = 6
                return self.handleRemoveProduct()
            elif(selection == 5):
                self.currentPage =7
                return self.handleGetRatings()
            elif (selection == 6):
                self.handleLogout()
                self.currentMenu = "landing"
            else:
                return self.handleBadResponse()
            
        return self.globalResponse
    
    def getProducts(self):
        # Set function invocation time
        self.globalResponse["invokeTime"] = time.time()

        # fetch seller id to be used in API call from seller class
        id = self.seller.id

        # API call
        products=self.products.getProductsBySeller(id)

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
        self.globalResponse["msg"] = productmessage + "Please press enter to go back to the menu"
        self.currentPage = 0
        return self.globalResponse
    
    def handleAddProduct(self, request_msg = None):
        self.globalResponse["invokeTime"] = time.time()
        if not request_msg:
            self.globalResponse["msg"] = "You are adding a new product. Please enter the following:\n"
            self.globalResponse["msg"]+= "Name of the product (32 characters): "
            self.globalResponse["invokeTime"] = None
            return self.globalResponse
        elif not self.products.name:
            self.products.name = request_msg
            self.globalResponse["msg"]= "\nCategory ( Choose a value 0-9 ): "
            self.globalResponse["invokeTime"] = None
            return self.globalResponse
        elif not self.products.category:
            self.products.category = request_msg
            self.globalResponse["msg"]= "\nCondition ( 1 - New or 2 - Used ): "
            self.globalResponse["invokeTime"] = None
            return self.globalResponse
        elif not self.products.condition:
            self.products.condition = 'New' if int(request_msg) ==1 else "Used"
            self.globalResponse["msg"]= "\nPrice: "
            self.globalResponse["invokeTime"] = None
            return self.globalResponse
        elif not self.products.price:
            self.products.price = request_msg
            self.globalResponse["msg"]= "\Quantity: "
            self.globalResponse["invokeTime"] = None
            return self.globalResponse
        elif not self.products.quantity:   
            self.products.quantity = request_msg  
            self.globalResponse["msg"]= "\nKeywords (At most 5, seperated by commas): "
            self.globalResponse["invokeTime"] = None
            return self.globalResponse
        elif not self.products.keywords:     
            self.products.keywords = request_msg.split(',')

        
        valid, msg = self.products.validateProduct()

        if not valid:
            self.globalResponse["msg"] = msg + "\nPlease try again. \n\nPress enter to get back to the main menu"
            return self.globalResponse
        
        newid = self.products.addProduct()
        self.globalResponse["msg"] = "Product added successfully!\n\nPress enter to get back to the main menu"
        self.currentPage = 0
        return self.globalResponse
        

    def handleEditProduct(self, request_msg = None):
        self.globalResponse["invokeTime"] = time.time()
        if not request_msg:
            self.globalResponse["msg"] = "To edit a product, please enter the following:\n"
            self.globalResponse["msg"]+= "ID of the product: "
            self.globalResponse["invokeTime"] = None
            return self.globalResponse
        elif not self.products.prodid:
            self.products.prodid = request_msg
            self.globalResponse["msg"]= "\nPrice: "
            self.globalResponse["invokeTime"] = None
            return self.globalResponse
        elif not self.products.price:
            self.products.price = request_msg

        self.products.sellerid = self.seller.id
        updated = self.products.editProduct()
        if updated == -1:
            self.globalResponse["msg"] = "The ID is incorrect. Please give a valid product ID. \n\nPress enter to get back to the main menu"
        else:
            self.globalResponse["msg"] = "Product edited successfully!\n\nPress enter to get back to the main menu"
        self.currentPage = 0
        return self.globalResponse

    def handleRemoveProduct(self, request_msg = None):
        self.globalResponse["invokeTime"] = time.time()
        if not request_msg:
            self.globalResponse["msg"] = "To remove a product, please enter the following:\n"
            self.globalResponse["msg"]+= "ID of the product: "
            self.globalResponse["invokeTime"] = None
            return self.globalResponse
        elif not self.products.prodid:
            self.products.prodid = request_msg

        self.products.sellerid = self.seller.id
        updated = self.products.removeProduct()
        print(updated)
        if updated == -1:
            self.products.clearProduct()
            self.globalResponse["msg"] = "The ID is incorrect. Please give a valid product ID. \n\nPress enter to get back to the main menu"
        else:
            self.globalResponse["msg"] = "Product removed successfully!\n\nPress enter to get back to the main menu"
        self.currentPage = 0
        return self.globalResponse
    
    def handleGetRatings(self):
        # No input needed
        self.globalResponse["invokeTime"] = time.time()

        # call api
        feedback = self.products.getRatings()

        #update seller feedback
        self.seller.updateFeedback(*feedback)
        # Give response to user
        self.globalResponse["msg"] = f"Your feedback is: \n Thumbs Ups: {feedback[0]} Thumbs Downs: {feedback[1]} \n\n Please press enter to go back to the menu"
        self.currentPage=0
        return self.globalResponse

    def handleLogin(self, request_msg=None ):

        self.globalResponse["invokeTime"] = time.time()

        if not request_msg:
            self.globalResponse["msg"] = "To login, please enter the following:\n"
            self.globalResponse["msg"]+= "Username: "
            self.globalResponse["invokeTime"] = None
            return self.globalResponse
        elif not self.seller.getUsername():
            self.seller.setUsername(request_msg)
            self.globalResponse["invokeTime"] = None
            self.globalResponse["msg"]= "\nPassword: "
            return self.globalResponse
        elif not self.seller.getPassword():     
            self.seller.setPassword(request_msg)
        
        # if not self.seller.validateUser(self._username,self._password):
        #     self.globalResponse["msg"] = "Please enter valid username and password"
        #     return self.globalResponse
        
        code, msg = self.seller.loginUser(self.seller._username,self.seller._password)
        if  code == 1:
            self.globalResponse["msg"] = f"Logged in for {self.seller.getUsername()} \nPress enter to go to the landing menu"
            self.LOGIN_STATUS = True
            self.products.sellerid = self.seller.id
            self.currentPage = 0
            self.currentMenu = 'landing'
        else:
            self.globalResponse["msg"] = msg + "\nPress enter to go back to menu"
            self.seller.clearUser()

        return self.globalResponse

    def handleRegistration(self, request_msg=None):

        self.globalResponse["invokeTime"] = time.time()
        # get inputs
        if not request_msg:
            self.globalResponse["invokeTime"] = None
            self.globalResponse["msg"] = "To create account, please enter the following:\n"
            self.globalResponse["msg"]+= "Username: "
            return self.globalResponse
        elif not self.seller.getUsername():
            self.seller.setUsername(request_msg)
            self.globalResponse["invokeTime"] = None
            self.globalResponse["msg"]+= "\nPassword(at least 6 letters): "
            return self.globalResponse
        elif not self.seller.getPassword():     
            self.seller.setPassword(request_msg)
        
        isValid, errmsg = self.seller.validateUser()
        if not isValid:
            self.globalResponse["msg"] = errmsg
            self.currentPage = 0
            self.seller.clearUser()
            return self.globalResponse

        # call api
        code, msg = self.seller.registerUser()

        # generate response based on api result
        if  code == 1:
            self.globalResponse["msg"] = f"Created Account for {self.seller.getUsername()} \nPress enter to go to the landing menu"
            self.products.sellerid = self.seller.id
            self.LOGIN_STATUS = True
            self.currentPage = 0
            self.currentMenu = 'landing'
        else:
            self.seller.clearUser()
            self.LOGIN_STATUS=False
            self.currentPage = 0
            self.currentMenu = 'home'
            self.globalResponse["msg"] = msg + "\nPress enter to go back to the menu"
        return self.globalResponse   

    def handleLogout(self, inactivity = False):
        self.LOGIN_STATUS = False
        self.seller.clearUser()
        if inactivity:
            self.currentPage=0
            return {"msg": "You were logged out because of inactivity. Please login again.\n\n" + self.getMenuMessage("home"), "invokeTime":None}
        self.globalResponse["msg"] = "Logging out...\n\n" + self.getMenuMessage("home")
        self.globalResponse["invokeTime"] = None

        
    def handleExit(self):
        self.products.cleandb()
        self.seller.cleandb()
        self.globalResponse["msg"] = "!DISCONNECT"
        self.globalResponse["invokeTime"] = None
    
    def handleBadResponse(self):
        self.globalResponse["msg"] = self.INCORRECT_INPUT_ERROR
        self.globalResponse["invokeTime"] = None

    def getResponse(self, msg, ):
        # redirect control to current function
        return self.pages[self.currentPage](msg)