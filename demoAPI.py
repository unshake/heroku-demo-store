from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, make_response
import jwt, datetime, re 
from validate_email import validate_email
from functools import wraps
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
#
# Email format verification function
def isEmailValid(email):
	return validate_email(email)
#Password fortmat verification function
def isPasswordValid(password):
	if len(password) >= 8:
		if not re.search('\s', password):
			if re.search(r"(?=.*[A-Z])(?=.*[*&@%+/'!#$?:,`_.\-])",password):
				return True
			else:
				return False
		else:
			return False
		
	else:
		return False
#Decorator para verificar logIn
def tokenOK(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = request.args.get('token')
		if not token:
			return jsonify({'message': 'Token is missing!'})
		try:
			data = jwt.decode(token, 'J0hnCu3vas80')
		except:
			return jsonify({'message': 'Token is invalid'})

		return f(*args, **kwargs)
	return decorated



#Creacion de los EndPoints de la API

@app.route('/')
@app.route('/api/v0/products/')
def showProducts():
	allProducts = session.query(Products)
	return jsonify(Products=[p.serialize for p in allProducts])

@app.route('/api/v0/products/user')
@tokenOK
def iShowProducts():
	allProducts = session.query(Products).all()
	return render_template('productsUser.html', products = allProducts)

@app.route('/api/v0/login/', methods=['GET', 'POST'])
def userLogIn():
	
	if request.method == 'POST':
		idUser = request.form['id']
		passUser = request.form['password']
		if idUser == "":
			return jsonify({'message':'Empty e-mail field. Please enter your e-mail.'})
		if passUser == "":
			return jsonify({'message':'Empty password field. Please enter your password'})
		if not isEmailValid(idUser): #verifico formato de e-mail
			return jsonify({'message':'Invalid e-mail format. FOLLOW the next format: example@example.com'})
		if not isPasswordValid(passUser): #verifico formato de password
			return jsonify({'message': "Invalid password format. It MUST include at least 8 characters, 1 Uppercase letter and 1 of the following symbols: *&@%+/'!#$?:,`_.-"})
		
		allUsers = session.query(Users).all()
		for user in allUsers:
			if user.id == idUser:
				if user.password == passUser:
					token = jwt.encode({'user': idUser}, 'J0hnCu3vas80')
					return jsonify({'token':token.decode('UTF-8')})
					
				else:
					return redirect(url_for('userLogIn'))
			
		return redirect(url_for('userRegister'))

	else:
		return render_template('LogIn.html')



@app.route('/api/v0/products/add', methods=['GET', 'POST'])
#@tokenOK
def addProducts():
	if request.method == 'POST':
		newProduct = Products(name = request.form['name'], id = request.form['id'], description = request.form['description'],
			price=request.form['price'], size=request.form['size'], brand=request.form['brand'], color=request.form['color'])
		session.add(newProduct)
		session.commit()
		
		return redirect(url_for('showProducts'))
	else:
		return render_template('addProducts.html')


@app.route('/api/v0/register/', methods=['GET', 'POST'])
def userRegister():
	if request.method == 'POST':
		nameUser = request.form['name']
		idUser = request.form['id']
		passUser = request.form['password']
		if nameUser == "":
			return jsonify({'message':'Empty Name field. Please provide a name.'})
		if idUser == "":
			return jsonify({'message':'Empty e-mail field. Please provide your user e-mail.'})
		if passUser == "":
			return jsonify({'message':'Empty password field. Please provide your password'})
		if not isEmailValid(idUser): #verifico formato de e-mail
			return jsonify({'message':'Invalid e-mail format. FOLLOW the next format: example@example.com'})
		if not isPasswordValid(passUser): #verifico formato de password
			return jsonify({'message': "Invalid password format. It MUST include at least 8 characters, 1 Uppercase letter and 1 of the following symbols: *&@%+/'!#$?:,`_.-"})
		newUser = Users(name = request.form['name'], id = request.form['id'], password = request.form['password'])
		session.add(newUser)
		session.commit()
		
		return redirect(url_for('userLogIn'))
	else:
		
		return render_template('userRegister.html')

@app.route('/api/v0/products/cart/')
def addToCart():
	return "To be implemented"

@app.route('/api/v0/users/show/')
def showUsers():
	allUsers = session.query(Users)
	return jsonify(Users=[u.serialize for u in allUsers])

@app.route('/api/v0/users/recovery/', methods=['GET', 'POST'])
def passwordRecovery():
	if request.method == 'POST':
		idUser = request.form['id']
		keyUser = request.form['keyword']
		if idUser == "":
			return jsonify({'message':'Empty e-mail field. Please provide your user e-mail.'})
		if keyUser == "":
			return jsonify({'message':'Empty keyword field. Please provide your user keyword.'})
		if not isEmailValid(idUser): #verifico formato de e-mail
			return jsonify({'message':'Invalid e-mail format. FOLLOW the next format: example@example.com'})
		toEditUser = session.query(Users).filter_by(id = idUser).scalar()
		
		if toEditUser: #Verifico si existe el usuario
			if toEditUser.keyword == keyUser:
				newPassword = request.form['newPassword']
				if newPassword == "":
					return jsonify({'message':'Empty password field. Please provide your password'})
				if not isPasswordValid(newPassword): #verifico formato de password
					return jsonify({'message': "Invalid password format. It MUST include at least 8 characters, 1 Uppercase letter and 1 of the following symbols: *&@%+/'!#$?:,`_.-"})
				if toEditUser.password != newPassword:
					toEditUser.password = newPassword
				else:
					return jsonify({'message': 'You have used that password before. Choose another one'})

		else:
			return jsonify({'message': 'User not found'})

		
		session.add(toEditUser)
		session.commit()
		return redirect(url_for('userLogIn'))

	else:
		return render_template('passwordRecovery.html')

@app.route('/api/v0/users/password/new/', methods=['GET', 'POST'])
def passwordNew():
	return "to be implemented"



if __name__ == '__main__':
	app.secret_key = 'super_secret'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)