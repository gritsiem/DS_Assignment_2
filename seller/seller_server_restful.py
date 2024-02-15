from flask import Flask, request, jsonify, redirect
from seller import SellerPortal
app = Flask(__name__)

portal = SellerPortal()

@app.route('/')
def home():
    
    return portal.getWelcomeMessage()

@app.route('/login', methods = ["POST"])
def login():
    if request.method == 'POST':
        print(request.data)
        username = request.form['username']
        password = request.form['password']
        return jsonify(portal.handleLogin(username,password))
    
@app.route('/register', methods = ["POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return jsonify(portal.handleRegistration(username,password))

@app.route('/products', methods = ["GET", "POST"])
def products():
    if request.method == 'GET':
        token = request.form['token']
        return jsonify(portal.getProducts(token))
    #     user = request.form['nm']
    if request.method == 'POST':
        token = request.form['token']
        name = request.form["name"]
        category = request.form["category"]
        condition = request.form["condition"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        keywords = request.form["keywords"]
          
        print("PRODUCTTT", name, category,condition,price,quantity,keywords)
        return jsonify(portal.handleAddProduct(token,name, category,condition,price,quantity,keywords))
    
@app.route('/products/<id>', methods = ["PUT", "DELETE"])
def product(id):
    if request.method == 'PUT':
        token = request.form['token']
        price = request.form['price']
        return jsonify(portal.handleEditProduct(token,id, price))
    if request.method == 'DELETE':
        token = request.form['token']
        return jsonify(portal.handleRemoveProduct(token,id))
    
@app.route('/ratings', methods = ["GET"])
def ratings():
    if request.method == 'GET':
        token = request.form['token']
        return jsonify(portal.handleGetRatings(token))
    
@app.route('/logout', methods = ["GET"])
def logout():
    if request.method == 'GET':
        # token = request.form['token']
        jsonify(portal.handleLogout())
        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)