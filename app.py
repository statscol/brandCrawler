from flask import Flask
from flask import render_template,request,url_for,redirect
import os
import requests
import re
import pytube
from auxiliar import yout_to_img

app=Flask(__name__)

@app.route("/")
@app.route("/home")

def home():
	return render_template('home.html',busc="Ingrese el enlace de Youtube aquí")

@app.route("/results",methods=['GET','POST'])
def results():
	busq=request.form.get('search')
	print(busq)
	if len(re.findall("youtube",busq))==0 and len(re.findall("youtu",busq))==0:
		return("No es un enlace de Youtube, por favor ingrese un enlace válido")
	else:
		yout_to_img(busq,'/home/jf/','vid')

		return ("El video con enlace {} ha sido descargado ".format(busq))


if __name__ == "__main__":

	app.run(debug=True,host="0.0.0.0",port=8080,threaded=True)