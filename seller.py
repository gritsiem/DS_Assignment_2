# from custdb import cust 
import hashlib
from customer_model import CustomerInterface
from products_model import ProductInterface
# class Seller:
#     def __init__(self, name ):
#         self.name = name
#         self.feedback={"thumbsup": 0 , "thumbsdown":0}
    

class Authentication:
    def __init__(self):
        self._username = None
        self._password = None
        self.id = None
        self._isLoggedIn = False
        self.db = CustomerInterface()
        self.LOGIN_ERROR = "Account creation failed, please try again."
    
    def registerUser(self):
        print(self._username) 
        print (self._password) 
        #contact customer db
        # if there's a customer with that name and password already
        # generate error
        # else
        # add user to the DB

        print("register flow working")
        if not self.db.getUser(self._username, self._password):
            self.id = self.db.insertCustomer(self._username, self._password)
            self._isLoggedIn = True
            return 1,"Success"
        else:
            return 2, self.LOGIN_ERROR

    def loginUser(self, un, pw):
        
        # try to get passwords
        # will need hashes otherwise both un and pw are possibily not unique. Anyway, doesnt matter
        # do not know the other information, but that is it.
        # if we get one unique result for this, we log the user in. Server is supposed to be stateless
        # so maybe store the logged in info on the DB? you're just not logged in
        user = self.db.getUser(self._username, self._password)
        
        if user:
            self._username == user["username"]
            self.id = user["id"]
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
        if len(self._username.strip())==0 or len(self._password.strip()) == 0:
            self.clearUser()
            return False
        else:
            return True
    def getHash(self,pw):
        return hashlib.sha256(pw.encode())
    
    def clearUser(self):
        self._username = None
        self._password = None
        

class Products:
    def __init__(self):
        self.proddb = ProductInterface()
        self.prodid = None
        self.sellerid = None
        self.name  = None
        self.category  = None
        self.condition = None
        self.price = None
        self.keywords = None
        self.sellerproduts = []

    def getProductsBySeller(self, sellerid):
        products = [] 
        # try:
        products = self.proddb.getproducts(sellerid)
            # self.table.append({"id": id, "productname": name,"category":category, "conditon" : condition, "price": price, "keywords": keywords})
        # except:
        #     print("there was an error")
        #     return -1
        self.clearProduct()
        # return self.prodid
        return products
    
    def addProduct(self):
        try:
            self.prodid = self.proddb.addProduct(self.sellerid,self.name,self.category, self.condition, self.price, self.keywords)
            # self.table.append({"id": id, "productname": name,"category":category, "conditon" : condition, "price": price, "keywords": keywords})
        except:
            print("there was an error")
            return -1
        self.clearProduct()
        return self.prodid
    
    def editProduct(self):
        # try:
        id = self.proddb.editProduct(self.prodid,self.price)
            # self.table.append({"id": id, "productname": name,"category":category, "conditon" : condition, "price": price, "keywords": keywords})
        # except:
        #     print("there was an error")
        #     return -1
        self.clearProduct()
        return id
    
    def removeProduct(self):
        try:
            id = self.proddb.removeProduct(self.prodid)
            # self.table.append({"id": id, "productname": name,"category":category, "conditon" : condition, "price": price, "keywords": keywords})
        except:
            print("there was an error")
            return -1
        self.clearProduct()
        return id
    
    def getRatings(self, sellerid):
        return self.proddb.getRatings(sellerid)
    
    def clearProduct(self):
        self.id = None
        self.sellerid = None
        self.name  = None
        self.category  = None
        self.condition = None
        self.price = None
        self.keywords = None

        

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
        self.currentMessage = ""
        self.pages={0:self.handleNavigation, 1: self.handleLogin, 2: self.handleRegistration, 3: self.getProducts, 4:self.handleAddProduct, 5: self.handleEditProduct, 6:self.handleRemoveProduct, 7:self.handleGetRatings}
        self.currentPage = 0
        self.INCORRECT_INPUT_ERROR = "Incorrect response. Please choose something else."
        self.auth = Authentication()
        self.products = Products()
        
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
        if len(selection) == 0:
            return self.getMenuMessage(self.currentMenu)
        selection = int(selection)
        
        if not self.LOGIN_STATUS:
            if(selection == 1):
                self.currentPage=1
                return self.handleLogin()
            elif (selection==2):
                self.currentPage=2
                print("Going to registration page:..")
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
            
        return self.currentMessage
    
    def getProducts(self):
        id = self.auth.id
        products=self.products.getProductsBySeller(id)
        # print("[product catalalogue]", products)
        productmessage=""
        for row in products:
            productmessage+=f" #{row[0]} - {row[1]} \n ------------\n Category: {row[2]} \n Condition: {row[3]}\n Price: {row[4]}\n\n"
        self.currentMessage = productmessage + "Please press enter to go back to the menu"
        self.currentPage = 0
        return self.currentMessage
    
    def handleAddProduct(self, request_msg = None):
        if not request_msg:
            self.currentMessage = "You are adding a new product. Please enter the following:\n"
            self.currentMessage+= "Name of the product (32 characters): "
            return self.currentMessage
        elif not self.products.name:
            self.products.name = request_msg
            self.currentMessage= "\nCategory ( Choose a value 0-9 ): "
            return self.currentMessage
        elif not self.products.category:
            self.products.category = request_msg
            self.currentMessage= "\nCondition ( write 'new' or 'used' ): "
            return self.currentMessage
        elif not self.products.condition:
            self.products.condition = request_msg
            self.currentMessage= "\nPrice: "
            return self.currentMessage
        elif not self.products.price:
            self.products.price = request_msg
            self.currentMessage= "\nKeywords (Seperate by commas): "
            return self.currentMessage
        elif not self.products.keywords:     
            self.products.keywords = request_msg

        self.products.sellerid = self.auth.id
        newid = self.products.addProduct()
        self.currentMessage = "Product added successfully!\n\nPress enter to get back to the main menu"
        self.currentPage = 0
        return self.currentMessage
        

    def handleEditProduct(self, request_msg = None):
        if not request_msg:
            self.currentMessage = "To edit a product, please enter the following:\n"
            self.currentMessage+= "ID of the product: "
            return self.currentMessage
        elif not self.products.prodid:
            self.products.prodid = request_msg
            self.currentMessage= "\nPrice: "
            return self.currentMessage
        elif not self.products.price:
            self.products.price = request_msg

        self.products.sellerid = self.auth.id
        self.products.editProduct()
        self.currentMessage = "Product edited successfully!\n\nPress enter to get back to the main menu"
        self.currentPage = 0
        return self.currentMessage

    def handleRemoveProduct(self, request_msg = None):
        if not request_msg:
            self.currentMessage = "To remove a product, please enter the following:\n"
            self.currentMessage+= "ID of the product: "
            return self.currentMessage
        elif not self.products.prodid:
            self.products.prodid = request_msg

        self.products.sellerid = self.auth.id
        self.products.removeProduct()
        self.currentMessage = "Product removed successfully!\n\nPress enter to get back to the main menu"
        self.currentPage = 0
        return self.currentMessage
    
    def handleGetRatings(self):
        feedback = self.products.getRatings(self.auth.id)
        self.currentMessage = f"Your feedback is: \n Thumbs Ups: {feedback[0]} Thumbs Downs: {feedback[1]} \n\n Please press enter to go back to the menu"
        self.currentPage=0
        return self.currentMessage

    def handleLogin(self, request_msg=None ):
        # print("login function")
        # self.currentMessage = "Login"
        if not request_msg:
            self.currentMessage = "To login, please enter the following:\n"
            self.currentMessage+= "Username: "
            return self.currentMessage
        
        elif not self.auth.getUsername():
            self.auth.setUsername(request_msg)
            self.currentMessage+= "\nPassword: "
            return self.currentMessage
        elif not self.auth.getPassword():     
            self.auth.setPassword(request_msg)
        
        # if not self.auth.validateUser(self._username,self._password):
        #     self.currentMessage = "Please enter valid username and password"
        #     return self.currentMessage
        
        code, msg = self.auth.loginUser(self.auth._username,self.auth._password)
        if  code == 1:
            self.currentMessage = f"Logged in for {self.auth.getUsername()} \nPress enter to go to the landing menu"
            self.LOGIN_STATUS = True
            self.currentPage = 0
            self.currentMenu = 'landing'
        else:
            self.currentMessage = msg + "\nPress enter to go back to menu"

        return self.currentMessage

    def handleRegistration(self, request_msg=None):
        # print("Register function")
        if not request_msg:
            self.currentMessage = "To create account, please enter the following:\n"
            self.currentMessage+= "Username: "
            return self.currentMessage
        elif not self.auth.getUsername():
            self.auth.setUsername(request_msg)
            self.currentMessage+= "\nPassword: "
            return self.currentMessage
        elif not self.auth.getPassword():     
            self.auth.setPassword(request_msg)
        
        # if not self.auth.validateUser(self._username,self._password):
        #     self.currentMessage = "Please enter valid username and password"
        #     return self.currentMessage
        
        code, msg = self.auth.registerUser()
        if  code == 1:
            self.currentMessage = f"Created Account for {self.auth.getUsername()} \nPress enter to go to the landing menu"
            self.LOGIN_STATUS = True
            self.currentPage = 0
            self.currentMenu = 'landing'
        else:
            self.currentMessage = msg + "\nPress enter to go back to the menu"
        return self.currentMessage  

    def handleLogout(self):
        self.LOGIN_STATUS = False
        self.auth.clearUser()
        self.currentMessage = "Logging out...\n\n" + self.getMenuMessage("home")
        
    def handleExit(self):
        # print("Exiting portal...")
        self.currentMessage = "!DISCONNECT"
    
    def handleBadResponse(self):
        # print("bad response function")
        self.currentMessage = self.INCORRECT_INPUT_ERROR

    def getResponse(self, msg):
        print(self.currentPage)
        return self.pages[self.currentPage](msg)