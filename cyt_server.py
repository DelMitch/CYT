#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response
from flask_pymongo import PyMongo
import json

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'temps'
mongo = PyMongo(app)

@app.route('/', methods = ['GET', 'POST'])
def index():
	if request.method == 'POST':
		return redirect(url_for('suggest'))
	elif request.method == 'GET':
		return render_template('index.html')

@app.route('/suggestion', methods = ['GET', 'POST'])
def suggest():
	zipcode = request.form['zipcode']
	lastcheck = request.form['lastcheck']
	
	print(lastcheck)
	# api stuff
	# database stuff

	all = get_all_temps()
	#print(all)

	add_to_db('2018-11-10', 23, 19)
	result = { 'yyyy' : '2018', 'month' : 'December', 'dd' : '05'}

	return render_template('suggest.html', result = result, all = all)

def add_to_db(date, high, low):
	mongo.db.tf.insert({'date' : date, 'high' : high, 'low' : low})

def get_all_temps():
	temps = mongo.db.tf.find({})
	temps_list = []

	for temp in temps:
		temps_list.append( {'date' : temp['date'], 'high' : temp['high'], 'low' : temp['low']} )

	return temps_list


if __name__ == '__main__':
	app.run()
