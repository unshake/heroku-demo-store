from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, make_response
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

#Creacion de los EndPoints de la API

@app.route('/')
@app.route('/api/v0/products/')
def unloggedUser_Products:
	allProducts = session.query(Products)
	return jsonify(Products=[p.serialize for p in allProducts])

@app.route('/api/v0/login/')
def userLogIn(user_id, user_password):
	return "To be implemented"


@app.route('/api/v0/products/<string:user_id>')
def loggedUser_Products(user_id):
	return "To be implemented"

@app.route('/api/v0/register/')
def userRegister(user_id, user_password):
	return "To be implemented"





if __name__ == '__main__':
	app.secret_key = 'super_secret'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)