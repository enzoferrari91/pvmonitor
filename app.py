from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import g

import sqlite3
import time
from datetime import datetime, timedelta
import config

# FLASK APP
app = Flask(__name__)

def extracttime(s):
  start = s.index(" ")
  return s[(start+1):(start+6)]

def extractdate(s):
	end = s.index(" ")
	return s[:end]

# Get current date (e.g. 2015-11-20)
def getDateToday():
	dateToday = time.strftime("%Y-%m-%d")
	return(dateToday)

# Get yesterday's and tommorow's date
def getDates(dateDB):
	dateToday = datetime.strptime(dateDB,"%Y-%m-%d") # Type 'Datetime'
	dateYesterday = dateToday - timedelta(days=1) 	 # Type 'Datetime'
	dateTomorrow = dateToday + timedelta(days=1) 	 # Type 'Datetime'

	dateYesterday = datetime.strftime(dateYesterday,"%Y-%m-%d") # Type 'String'
	dateTomorrow = datetime.strftime(dateTomorrow,"%Y-%m-%d")	# Type 'String'

	return(dateYesterday, dateTomorrow)

# Get power data from SQLite3
def selectPowerDB(dateDB):
	cur = g.db.cursor()
	cur.execute("SELECT * FROM powerLog WHERE datetime LIKE ?", (dateDB+'%' ,))
	data = cur.fetchall()
	
	# Create lists
	power_bez = list(zip(*data)[1])
	power_einsp = list(zip(*data)[2])
	power_pv = list(zip(*data)[3])
	timestampList = list(zip(*data)[0])
	timestampList = [str(x) for x in timestampList]
	timestampList = [extracttime(x) for x in timestampList]
		
	# Return the lists
	return (power_bez, power_einsp, power_pv, timestampList)

# Get energy data from SQLite3
def selectEnergyDB(year=0, mode="sum"):
	cur = g.db.cursor()
	if year == 0:
		cur.execute("SELECT * FROM dayLog")
		data = cur.fetchall()
	else:
		cur.execute("SELECT * FROM dayLog WHERE datetime LIKE ?", (year+'%' ,))
		data = cur.fetchall()
	
	if mode == "sum":
		list_energy_pv = list(zip(*data)[3])
		total_energy_pv = sum(list_energy_pv)
		return(total_energy_pv)
	else:
		list_energy_pv = list(zip(*data)[3])
		timestampList = list(zip(*data)[0])
		timestampList = [str(x) for x in timestampList]
		timestampList = [extractdate(x) for x in timestampList]
		return(list_energy_pv, timestampList)

@app.route("/")
@app.route("/<dateURL>")
def index(dateURL=getDateToday()):

 	# get date from URL
	try:
		dateDB = dateURL
	
	except:
		dateDB = getDateToday()

	dateYesterday, dateTomorrow = getDates(dateDB)

	try:
		power_bez, power_einsp, power_pv, timestampList = selectPowerDB(dateDB)
		actual_power_pv = power_pv[-1] # last entry in list
		today_energy_pv = round( sum([(i/12)/1000 for i in power_pv]), 1 ) # 5 minute intervall = factor 12

		total_energy_pv = selectEnergyDB()

		power_pv.extend((288-len(power_pv))*[0])
		timestampList.extend((288-len(timestampList))*[""])

	except:
		power_bez = []
		power_einsp = []
		power_pv = []
		timestampList = []
		actual_power_pv = 0
		today_energy_pv = 0
		total_energy_pv = 0
	

	return render_template("index.html", power_pv=power_pv, actual_power_pv=actual_power_pv, today_energy_pv=today_energy_pv,
		total_energy_pv=total_energy_pv, timestampList=timestampList, dateDB=dateDB,
		dateYesterday=dateYesterday, dateTomorrow=dateTomorrow)

@app.route("/energystats")
def energystats():
	list_energy_pv, timestampList = selectEnergyDB(mode="list")
	return render_template("energystats.html", list_energy_pv=list_energy_pv, timestampList=timestampList)

@app.route("/tables")
def tables():
	return render_template("tables.html")

@app.route("/showtables", methods=['POST'])
def showtables():
	dateDB = request.form['text']
	power_bez, power_einsp, power_pv, timestampList = selectPowerDB(dateDB)
	power_pv_tablelist = zip(power_pv,timestampList)
	return render_template("showtables.html", power_pv_tablelist=power_pv_tablelist)


@app.route("/system_messages")
def system_messages():
	return render_template("system_messages.html")

@app.before_request
def before_request():
	g.db = sqlite3.connect(config.dbfilepath)

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()

if __name__ == "__main__":
	if config.webserver == "MacOSX":
		app.run(host='0.0.0.0', debug=True)
	if config.webserver == "Raspberry":
		app.run(host='0.0.0.0', port=80)
