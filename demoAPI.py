from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, make_response
import jwt
import datetime
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
def unloggedUser_Products():
	allProducts = session.query(Products)
	return jsonify(Products=[p.serialize for p in allProducts])

@app.route('/api/v0/login/', methods=['GET', 'POST'])
def userLogIn():
	
	if request.method == 'POST':
		idUser = request.form['id']
		passUser = request.form['password']
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



@app.route('/api/v0/products/user')
@tokenOK
def loggedUser_Products():
	return "You have access"

@app.route('/api/v0/register/')
def userRegister():
	return "To be implemented"





if __name__ == '__main__':
	app.secret_key = 'super_secret'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)