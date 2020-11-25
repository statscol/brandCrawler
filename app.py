from flask import Flask
from flask import render_template,request,url_for,redirect
import os
import requests
import re
import pytube
import datetime
from auxiliar import yout_to_detections,get_brand_expo

DARKNET_PATH="/home/jf/yolov4/darknet/"
ROOT_DIR='/home/jf/'

app=Flask(__name__)



@app.route("/")
@app.route("/home")

def home():
	return render_template('home.html',busc="Ingrese el enlace de Youtube aquí")

@app.route("/results",methods=['GET','POST'])
def results():
	inicio=datetime.datetime.now()
	busq=request.form.get('search')
	print(busq)
	if len(re.findall("youtube",busq))==0 and len(re.findall("youtu",busq))==0:
		return("No es un enlace de Youtube, por favor ingrese un enlace válido")
	else:
		det_name=yout_to_detections(busq,ROOT_DIR,'vid',DARKNET_PATH=DARKNET_PATH)
		detections=get_brand_expo(det_name)
		print("elapsed time {:.2f} seconds".format((datetime.datetime.now()-inicio).total_seconds()))
		print(detections)
		return (detections)
		#return render_template('results.html',dat=detections)


if __name__ == "__main__":

	app.run(debug=True,host="0.0.0.0",port=8080,threaded=True)