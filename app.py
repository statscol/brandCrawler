from flask import Flask
from flask import render_template
import os


app=Flask(__name__)

@app.route("/")
@app.route("/home")

def home():
	return render_template('home.html',busc="Ingrese el enlace de Youtube aquí")

@app.route("/Results")
def results():
	return ("test")


if __name__ == "__main__":

	app.run(debug=True,host="0.0.0.0",port=8080,threaded=True)