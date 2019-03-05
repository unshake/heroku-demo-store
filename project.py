from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Users, Products, ShoppingCart

app = Flask(__name__)
CORS(app)

engine = create_engine('sqlite:///demostore_flask.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Codigo para enviar informacion en JSON

@app.route('/home/products/all')
def allStoreProductsJSON():
	allProducts = session.query(Products)
	return jsonify(Products=[p.serialize for p in allProducts])


@app.route('/home/users/<string:api_key>') #/home/users/all&key=API_KEY
def allStoreUsersJSON(api_key):
	keyDecoded = api_key.split("&key=")
	if keyDecoded[0] == "all":
		if keyDecoded[1] == "DemoStoreKey":
			allUsers = session.query(Users)
			return jsonify(Users=[u.serialize for u in allUsers])
		else:
			output = "<html><body><h1>You are not alowed to access this information!!!</h1></body></html>"
			return output
	else:
		output = "<html><body><h1>Incorrect EndPoint!</h1></body></html>"
		return output


@app.route('/home/users/id/<string:user_id>')
def oneStoreUserJSON(user_id):
	keyDecoded = user_id.split("&key=")
	user_id = keyDecoded[0]
	api_key = keyDecoded[1] 
	if api_key == "DemoStoreKey":
		selectedUser = session.query(Users).filter_by(id=user_id).one()
		return jsonify(User=selectedUser.serialize)

	else:
		output = "<html><body><h1>You are not alowed to access this information!</h1></body></html>"
		return output


@app.route('/home/products/brand/<string:product_brand>')
def oneStoreProductJSON(product_brand):
	selectedProduct = session.query(Products).filter_by(brand=product_brand).one()
	return jsonify(Product=selectedProduct.serialize)
	

#Estos son los endpoints de la aplicacion

@app.route('/')
@app.route('/home/')
def homeStore():
	return render_template('home.html')



@app.route('/home/products/')
def showProducts():
	allProducts = session.query(Products).all()
	return render_template('products.html', products = allProducts)

@app.route('/home/products/cart/')
def addToCart():
	return "To be implemented"
	

@app.route('/home/products/<string:user_name>/userShop/')
def userShop(user_name):
	allProducts = session.query(Products).all()
	return render_template('userShop.html', userName = user_name, products = allProducts)
	

@app.route('/home/signIn/', methods=['GET', 'POST'])
def signIn():
	if request.method == 'POST':
		idUser = request.form['id']
		passUser = request.form['password']
		allUsers = session.query(Users).all()
		for user in allUsers:
			if user.id == idUser:
				if user.password == passUser:
					myName = user.name.split(' ')
					return redirect(url_for('userShop', user_name = myName[0]))
					
				else:
					#flash("Wrong Password")
					return redirect(url_for('signIn'))
			
		return redirect(url_for('signUp'))
				
		
	else:
		return render_template('signIn.html')

@app.route('/home/signUp/', methods=['GET', 'POST'])
def signUp():
	if request.method == 'POST':
		newUser = Users(name = request.form['name'], id = request.form['id'], password = request.form['password'])
		session.add(newUser)
		session.commit()
		#flash("New menu item created!")
		return redirect(url_for('signIn'))
	else:
		return render_template('signUp.html')


if __name__ == '__main__':
	app.secret_key = 'super_secret'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)