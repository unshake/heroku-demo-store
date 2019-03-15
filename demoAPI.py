from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, make_response
import jwt, datetime, re 
from validate_email import validate_email
from functools import wraps
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Users, Products, ShoppingCart, tokenBlackList

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
			isTokenBlackListed = session.query(tokenBlackList).filter_by(token=token).scalar()
			if isTokenBlackListed:
				return jsonify({'message': 'Token is invalid. Please log in again.'})
			else:
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
	token = request.args.get('token')
	allProducts = session.query(Products).all()
	return render_template('productsUser.html', products = allProducts, userToken = token)
	
@app.route('/api/v0/login/', methods=['GET', 'POST'])
def userLogIn():
	
	if request.method == 'POST':
		idUser = request.form['id']
		passUser = request.form['password']
		if idUser == "":
			return jsonify({'message':'Empty e-mail field. Please enter your e-mail.'})
		if passUser == "":
			return jsonify({'message':'Empty password field. Please enter your password'})
		
		allUsers = session.query(Users).all()
		for user in allUsers:
			if user.id == idUser:
				if user.password == passUser:
					token = jwt.encode({'user': idUser, 
						'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
						'iat': datetime.datetime.utcnow()}, 
						'J0hnCu3vas80')
					return jsonify({'token':token.decode('UTF-8')})
					
				else:
					return redirect(url_for('userLogIn'))
			
		return redirect(url_for('userRegister'))

	else:
		return render_template('LogIn.html')

@app.route('/api/v0/logout/<string:logOutToken>')
def userLogOut(logOutToken):
	blacklistNewToken = tokenBlackList(token=logOutToken)
	session.add(blacklistNewToken)
	session.commit()
	return jsonify({'message':'Logged Out'})


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
		userKey = request.form['keyword']
		if nameUser == "":
			return jsonify({'message':'Empty Name field. Please provide a name.'})
		if idUser == "":
			return jsonify({'message':'Empty e-mail field. Please provide your user e-mail.'})
		if passUser == "":
			return jsonify({'message':'Empty password field. Please provide your password'})
		if userKey == "":
			return jsonify({'message':'Empty keyword field. Please provide a keyword for Password Recovery'})
		if not isEmailValid(idUser): #verifico formato de e-mail
			return jsonify({'message':'Invalid e-mail format. FOLLOW the next format: example@example.com'})
		if not isPasswordValid(passUser): #verifico formato de password
			return jsonify({'message': "Invalid password format. It MUST include at least 8 characters, 1 Uppercase letter and 1 of the following symbols: *&@%+/'!#$?:,`_.-"})
		
		try:
			newUser = Users(name = nameUser, id = idUser, password = passUser, keyword = userKey)
			session.add(newUser)
			session.commit()
		
		except:
			return jsonify({'message': 'There is a problem with inserting data to the database.'})

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
				return jsonify({'message': 'Wrong keyword!'})
		else:
			return jsonify({'message': 'User not found'})

		try:

			session.add(toEditUser)
			session.commit()
		except:
			return jsonify({'message': 'There is a problem with inserting data to the database'})

		
		return redirect(url_for('userLogIn'))

	else:
		return render_template('passwordRecovery.html')





if __name__ == '__main__':
	app.secret_key = 'super_secret'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)