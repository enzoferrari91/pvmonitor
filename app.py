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
import forecast

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

# Get tommorow's date
def getDates(dateDB):
	dateToday = datetime.strptime(dateDB,"%Y-%m-%d") # Type 'Datetime'
	dateTomorrow = dateToday + timedelta(days=1) 	 # Type 'Datetime'
	dateTomorrow = datetime.strftime(dateTomorrow,"%Y-%m-%d")	# Type 'String'

	return(dateTomorrow)

def average(data):
	l = len(data)
	temp = list()
	temp.append(data[0])
	for i in range(1,l):
		x = (data[i-1] + data[i]) / 2
		temp.append(x)
	
	data = temp
	return(data)		

# Get power data from SQLite3
def selectPowerDB(date_from_DB, date_to_DB):
	cur = g.db.cursor()
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
def selectEnergyDB(year="0", mode="sum"):
	cur = g.db.cursor()
	if year == "0":
		cur.execute("SELECT * FROM dayLog")
		data = cur.fetchall()
	else:
		cur.execute("SELECT * FROM dayLog WHERE datetime LIKE ?", (year+'%' ,))
		data = cur.fetchall()

	# Default mode "sum" 
	if mode == "sum":
		list_energy_bez = list(zip(*data)[1])
		list_energy_einsp = list(zip(*data)[2])
		list_energy_pv = list(zip(*data)[3])

		list_energy_bez = [0 if x is None else x for x in list_energy_bez]
		list_energy_einsp = [0 if x is None else x for x in list_energy_einsp]

		total_energy_bez = sum(list_energy_bez)
		total_energy_einsp = sum(list_energy_einsp)
		total_energy_pv = sum(list_energy_pv)
		return(total_energy_bez, total_energy_einsp, total_energy_pv)
	# Mode "list"
	else:
		list_energy_bez = list(zip(*data)[1])
		list_energy_einsp = list(zip(*data)[2])
		list_energy_pv = list(zip(*data)[3])
		timestampList = list(zip(*data)[0])
		timestampList = [str(x) for x in timestampList]
		timestampList = [extractdate(x) for x in timestampList]
		return(list_energy_bez, list_energy_einsp, list_energy_pv, timestampList)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/analyse")
def analyse():
	return render_template("analyse.html")

@app.route("/energystats")
@app.route("/energystats/<year>")
def energystats(year="2017"):
	list_energy_bez, list_energy_einsp, list_energy_pv, timestampList = selectEnergyDB(year=year, mode="list")
	list_energy_bez = [0 if x is None else x for x in list_energy_bez]
	list_energy_einsp = [0 if x is None else x for x in list_energy_einsp]

	# Berechnung Eigenverbrauchsquote pro Tag ################################
	list_ev_quote = list()

	for i in range(0,len(timestampList)):
		try:
			ev_quote = (1 - (list_energy_einsp[i] / list_energy_pv[i])) * 100
			ev_quote = round(ev_quote,0)
			list_ev_quote.append(ev_quote)
		except:
			list_ev_quote.append(0)
	#########################################################################

	total_energy_bez = sum(list_energy_bez)
	total_energy_einsp = sum(list_energy_einsp)
	total_energy_pv = sum(list_energy_pv)

	##### TOTAL SAVINGS #####################################################
	price_bezug = 0.18
	price_einsp = 0.029
	total_savings = (total_energy_pv - total_energy_einsp) * price_bezug + total_energy_einsp * price_einsp

	months = ["01","02","03","04","05","06","07","08","09","10","11","12"]
	list_month_energy_bez = list()
	list_month_energy_einsp = list()
	list_month_energy_pv = list()

	for month in months:
		try:
			month_energy_bez, month_energy_einsp, month_energy_pv = selectEnergyDB(year=(year+"-"+month), mode="sum")
		except:
			month_energy_bez = 0
			month_energy_einsp = 0
			month_energy_pv = 0

		list_month_energy_bez.append(month_energy_bez)
		list_month_energy_einsp.append(month_energy_einsp)
		list_month_energy_pv.append(month_energy_pv)

	# Berechnung Eigenverbrauchsquote und Ersparnisse pro Monat ################################
	list_ev_quote_month= list()
	list_savings_month= list()
	for i in range(0,len(months)):
		try:
			ev_quote_month = (1 - (list_month_energy_einsp[i] / list_month_energy_pv[i])) * 100
			ev_quote_month = round(ev_quote_month,0)
			list_ev_quote_month.append(ev_quote_month)
			savings_month = (list_month_energy_pv[i] - list_month_energy_einsp[i]) * price_bezug + list_month_energy_einsp[i] * price_einsp
			list_savings_month.append(savings_month)
		except:
			list_ev_quote_month.append(0)
			list_savings_month.append(0)
	############################################################################

	return render_template("energystats.html", 
							list_energy_pv=list_energy_pv, list_energy_bez=list_energy_bez, 
							list_energy_einsp=list_energy_einsp,
							list_ev_quote = list_ev_quote, 
							total_energy_pv=total_energy_pv,
							total_energy_bez=total_energy_bez,
							total_energy_einsp=total_energy_einsp,
							total_savings=total_savings,
							timestampList=timestampList,
							list_month_energy_bez=list_month_energy_bez,
							list_month_energy_einsp=list_month_energy_einsp,
							list_month_energy_pv=list_month_energy_pv,
							list_ev_quote_month=list_ev_quote_month,
							list_savings_month=list_savings_month,
							months=months)

@app.route("/system_messages")
def system_messages():
	return render_template("system_messages.html")

@app.route("/msg/<msg>")
def msg(msg):
	f = open((config.logfilepath + msg) , 'r')
	s = f.read()
	f.close()
	return(s)

@app.route("/check_missing_data")
def check_missing_data():
	#date_from_DB = "2016-11-01" # Start of operation
	date_from_DB = "2017-01-01"	 # New year
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
		d_next = getDates(d)
		try:
			power_bez, power_einsp, power_pv, timestampList = selectPowerDB(d,d_next)
			if not(len(power_bez) == 288 & len(power_einsp) == 288 & len(power_pv) == 288):
				missing = missing + d + "<br>"
		except:
			missing = missing + d + "<br>"
	if missing == "":
		output = "All datasets OK - No missing data"
	else:
		output = "Missing data:<br>" + missing

	return(output)

@app.route("/alarmprotokoll")
def alarmprotokoll():
	f = open(config.alarmfilepath, 'r')
	s = f.read()
	s=s.replace ('\n', '<br>')
	f.close()
	return(s)

@app.route("/_get_data")
def showtimeseriesJSON():
    date_from_DB = request.args.get('dateselect_from')
    date_to_DB = request.args.get('dateselect_to')

    date_to_DB = getDates(date_to_DB)

    try:
    	power_bez, power_einsp, power_pv, timestampList = selectPowerDB(date_from_DB,date_to_DB)
    	power_bez = [0 if x is None else x for x in power_bez]
    	power_einsp = [0 if x is None else x for x in power_einsp]

    	actual_power_bez = power_bez[-1]
    	actual_power_einsp = power_einsp[-1]
    	actual_power_pv = power_pv[-1] # last entry in list

    	today_energy_bez = round( sum([(i/12)/1000 for i in power_bez]), 1 ) # 5 minute intervall = factor 12
    	today_energy_einsp = round( sum([(i/12)/1000 for i in power_einsp]), 1 ) # 5 minute intervall = factor 12
    	today_energy_pv = round( sum([(i/12)/1000 for i in power_pv]), 1 ) # 5 minute intervall = factor 12
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
    	actual_power_bez = 0
    	actual_power_einsp = 0
    	actual_power_pv = 0
    	today_energy_bez = 0
    	today_energy_einsp = 0
    	today_energy_pv = 0

    # FORECAST MODUL #
    try:
    	fcast_pv,ghi_API,cloud,temp,ghi = forecast.forecast(date_from_DB)

    	err = [0]*288
    	for i in range(0,288):
    		err[i] = power_pv[i] - fcast_pv[i]

    except:
    	fcast_pv = []
    	err = []
    	ghi_API = []
    	ghi = []
    	cloud = []
    	temp = []

    return jsonify(power_bez=power_bez, actual_power_bez=actual_power_bez, today_energy_bez=today_energy_bez, power_einsp=power_einsp, 
		actual_power_einsp=actual_power_einsp, 
		today_energy_einsp=today_energy_einsp,
		power_pv=power_pv, 
		actual_power_pv=actual_power_pv, 
		today_energy_pv=today_energy_pv, 
		timestampList=timestampList,
		fcast_pv=fcast_pv,
		ghi_API=ghi_API,
		cloud=cloud,
		temp=temp,
		ghi=ghi,
		err=err)	
    
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




