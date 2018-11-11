#!/usr/bin/env python

from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response
from flask_pymongo import PyMongo
import datetime
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

	old = False

	today = find_today()

	tsplit = today.split('-')
	dsplit = lastcheck.split('-')

	if int(tsplit[1]) - int(dsplit[1]) > 1:
		old = True
		result = { 'yyyy' : tsplit[0], 'month' : convert_month(int(tsplit[1])), 'dd' : tsplit[2]}
	elif int(tsplit[1]) - int(dsplit[1]) == 1 and int(tsplit[2]) + (30 - int(dsplit[2])) > 30:
		old = True
		result = { 'yyyy' : tsplit[0], 'month' : convert_month(int(tsplit[1])), 'dd' : tsplit[2]}
	elif res_in_db(lastcheck, zipcode) and not old:
		result_log = mongo.db.results.find_one({'date' : lastcheck, 'zip' : zipcode})
		rsplit = result_log['result'].split(' ')
		result = { 'yyyy' : rsplit[2], 'month' : rsplit[1], 'dd' : rsplit[0]}
	elif not res_in_db(lastcheck, zipcode) and not old:
		#check api to get data
		#add_to_db('2018-11-11', '99709', 26, 21)
		print("API TIME")
		#api_logs = mongo.db.tf.find({'date' : #after lastcheck, 'zip' : zipcode})
		#do calculations on the api_logs list
		#api_log = #final decision list
		#result = { 'yyyy' : asplit[0], 'month' : convert_month(int(asplit[1])), 'dd' : asplit[2]}

	result = { 'yyyy' : 'dummY', 'month' : 'duMmy', 'dd' : 'Dummy'}

	if old and res_in_db(lastcheck, zipcode):
		old = False
		update_results(lastcheck, zipcode, result['dd'] + ' ' + result['month'] + ' ' + result['yyyy'])
	
	if not res_in_db(lastcheck, zipcode):
		store_results(lastcheck, zipcode, result['dd'] + ' ' + result['month'] + ' ' + result['yyyy'])
	

	#all = get_all_temps()
	#print(all)
	#all2 = get_all_results()
	#print("all2", all2)

	return render_template('suggest.html', result = result, input = request.form)


def find_today():
	now = datetime.datetime.now()
	return now.strftime("%Y-%m-%d")


def convert_month(mm):
	switchit = {
		1: "January",
		2: "February",
		3: "March",
		4: "April",
		5: "May",
		6: "June",
		7: "July",
		8: "August",
		9: "September",
		10: "October",
		11: "November",
		12: "December"
	}
	
	return switchit.get(mm, "invalid month")


def res_in_db(date, zip):
	exists = mongo.db.results.find_one({'date' : date, 'zip' : zip})
	if exists == None:
		return False
	else:
		return True


def add_to_db(date, zip, high, low):
	mongo.db.tf.insert({'date' : date, 'zip' : zip, 'high' : high, 'low' : low})


def get_all_temps():
	temps = mongo.db.tf.find({})
	temps_list = []

	for temp in temps:
		temps_list.append( {'date' : temp['date'], 'zip' : temp['zip'], 'high' : temp['high'], 'low' : temp['low']} )

	return temps_list


def store_results(date, zip, result):
	mongo.db.results.insert({'date' : date, 'zip' : zip, 'result' : result})


def update_results(date, zip, new_result):
	updated_res = mongo.db.results.find_one_and_update({'date' : date, 'zip' : zip}, {"$set" : {'result' : new_result}}, upsert=True)


def get_all_results():
	results = mongo.db.results.find({})
	res_list = []

	for result in results:
		res_list.append( {'date' : result['date'], 'zip' : result['zip'], 'result' : result['result']} )

	return res_list


if __name__ == '__main__':
	app.run()