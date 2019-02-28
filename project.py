from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Users, Products, ShoppingCart

app = Flask(__name__)

engine = create_engine('sqlite:///demostore_flask.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Codigo para enviar informacion en JSON

@app.route('/home/products/JSON')
def storeProductsJSON():
	allProducts = session.query(Products)
	return jsonify(MenuItems=[p.serialize for p in allProducts])

#@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
#def restaurantMenuItemJSON(restaurant_id, menu_id):
#	
#	items = session.query(MenuItem).filter_by(id=menu_id).one()
#	return jsonify(MenuCosas=items.serialize)
	

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