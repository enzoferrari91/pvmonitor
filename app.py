from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import g
from flask import jsonify

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

def average(data):
	"""
	l = len(power_bez)
	for i in range(1,l):
		power_bez[i] = (power_bez[i-1] + power_bez[i]) / 2
	"""
	l = len(data)
	temp = list()
	temp.append(data[0])
	for i in range(1,l):
		x = (data[i-1] + data[i]) / 2
		temp.append(x)
	
	data = temp
	return(data)		

# Get power data from SQLite3
def selectPowerDB(date_from_DB, date_to_DB="", mode="day"):
	cur = g.db.cursor()

	# Default mode "day"
	if mode =="day":
		cur.execute("SELECT * FROM powerLog WHERE datetime LIKE ?", (date_from_DB+'%' ,))
		data = cur.fetchall()
	# Mode "daterange"
	else:
		cur.execute("SELECT * FROM powerLog WHERE datetime >= ? and datetime < ?", (date_from_DB, date_to_DB))
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

	# Default mode "sum" 
	if mode == "sum":
		list_energy_pv = list(zip(*data)[3])
		total_energy_pv = sum(list_energy_pv)
		return(total_energy_pv)
	# Mode "list"
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

		actual_power_bez = power_bez[-1]
		actual_power_einsp = power_einsp[-1]
		actual_power_pv = power_pv[-1] # last entry in list

		today_energy_bez = round( sum([(i/12)/1000 for i in power_bez]), 1 ) # 5 minute intervall = factor 12
		today_energy_einsp = round( sum([(i/12)/1000 for i in power_einsp]), 1 ) # 5 minute intervall = factor 12
		today_energy_pv = round( sum([(i/12)/1000 for i in power_pv]), 1 ) # 5 minute intervall = factor 12

		total_energy_pv = selectEnergyDB()

		power_bez = average(power_bez)
		power_einsp = average(power_einsp)

		power_bez.extend((288-len(power_bez))*[0])
		power_einsp.extend((288-len(power_einsp))*[0])
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
	

	return render_template("index.html", 
		power_bez=power_bez, 
		actual_power_bez=actual_power_bez, 
		today_energy_bez=today_energy_bez,
		power_einsp=power_einsp, 
		actual_power_einsp=actual_power_einsp, 
		today_energy_einsp=today_energy_einsp,
		power_pv=power_pv, 
		actual_power_pv=actual_power_pv, 
		today_energy_pv=today_energy_pv,
		total_energy_pv=total_energy_pv, 
		timestampList=timestampList, dateDB=dateDB,
		dateYesterday=dateYesterday, dateTomorrow=dateTomorrow)

@app.route("/energystats")
def energystats():
	list_energy_pv, timestampList = selectEnergyDB(mode="list")
	return render_template("energystats.html", list_energy_pv=list_energy_pv, timestampList=timestampList)

@app.route("/tables")
def tables():
	return render_template("tables.html")

@app.route("/timeseries")
def timeseries():
	return render_template("timeseries.html")

@app.route("/showtables", methods=['POST'])
def showtables():
	dateDB = request.form['dateselect']
	power_bez, power_einsp, power_pv, timestampList = selectPowerDB(dateDB)

	max_power_pv = max(power_pv)
	power_pv_tablelist = zip(power_pv,timestampList)
	return render_template("showtables.html", power_pv_tablelist=power_pv_tablelist, max_power_pv=max_power_pv)

@app.route("/showtimeseries", methods=['POST'])
def showtimeseries():
	date_from_DB = request.form['dateselect_from']
	date_to_DB = request.form['dateselect_to']
	temp, date_to_DB = getDates(date_to_DB)

	try:
		power_bez, power_einsp, power_pv, timestampList = selectPowerDB(date_from_DB,date_to_DB,mode="range")

	except:
		power_bez = []
		power_einsp = []
		power_pv = []
		timestampList = []

	return render_template("showtimeseries.html", power_pv=power_pv, timestampList=timestampList)

@app.route("/system_messages")
def system_messages():
	date_from_DB = "2016-11-01" # Start of operation
	date_to_DB = getDateToday()

	missing = ""

	date_from_DB = datetime.strptime(date_from_DB,"%Y-%m-%d")
	date_to_DB = datetime.strptime(date_to_DB,"%Y-%m-%d")

	delta = (date_to_DB - date_from_DB).days
	datelist = list()

	for i in range(0,delta):
		newdate = date_from_DB + timedelta(days=i)
		datelist.append(datetime.strftime(newdate,"%Y-%m-%d"))
	
	for d in datelist:
		power_bez, power_einsp, power_pv, timestampList = selectPowerDB(d)

		if not(len(power_bez) == 288 & len(power_einsp) == 288 & len(power_pv) == 288):
			missing = missing + d + "; "

	if missing == "":
		output = "All datasets OK - No missing data"
	else:
		output = "Missing data: " + missing
	
	return render_template("system_messages.html", output=output)

@app.route("/msg/<msg>")
def msg(msg):
	f = open((config.logfilepath + msg) , 'r')
	s = f.read()
	f.close()
	return(s)


@app.route("/_get_data")
def add_numbers():
    #dateselect_from = request.args.get('dateselect_from')
    #dateselect_to = request.args.get('dateselect_to')

    data_activity = config.activity
    return jsonify(**data_activity)


    #return jsonify(result="OK")

@app.route("/sync")
def sync():
	return render_template("synchr.html")

@app.route("/jsonTest")
def jsonTest():
	return render_template("jsonTest.html")


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
