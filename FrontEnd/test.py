from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/testLogIn/', methods=['GET', 'POST'])
def testLogIn():
	return render_template('testLogIn.html')

@app.route('/testRegister/', methods=['GET', 'POST'])
def testRegister():
	return render_template('testUserRegister.html')








if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5000)