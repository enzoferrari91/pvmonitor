import sqlite3
import config

def forecast(date_from_DB):
	interval = 36

	# +++ Forecast coefficients +++ #
	beta3 = -8.2e-6
	beta2 = 0.013
	beta1 = -0.09

	db = sqlite3.connect(config.dbfilepath)
	cur = db.cursor()

	cur.execute("SELECT * FROM forecastLogAPI WHERE datetime LIKE ?", (date_from_DB+'%' ,))
	data = cur.fetchall()

	ghi_API = list(zip(*data)[1])


	db.close()

	length = len(ghi_API)
	ghi_API_interpol = list()
	ghi_API_interpol.extend([0]*24)
	ghi_API_interpol.append(ghi_API[0])

	for i in range(0,length-1):

		z = i + 1

		for j in range(1,interval):
			y = ghi_API[i] + (ghi_API[z] - ghi_API[i]) / interval * j
			ghi_API_interpol.append(y)

		ghi_API_interpol.append(ghi_API[z])

	ghi_API_interpol.extend([0]*23)


	#################################################################################################################################
	#interval = 12

	#db = sqlite3.connect(config.dbfilepath)
	#cur = db.cursor()

	#cur.execute("SELECT * FROM forecastLog WHERE datetime LIKE ?", (date_from_DB+'%' ,))
	#data = cur.fetchall()

	#                       1 for cloud / 5 for ghi
	#cloud = list(zip(*data)[5])
	#cc = list(zip(*data)[1])
	#cc_mean = sum(cc) / len(cc)

	#db.close()

	#length = len(cloud)
	#cloud_interpol = list()
	#cloud_interpol.extend([0]*12)
	#cloud_interpol.append(cloud[0])

	#for i in range(0,length-1):

	#	z = i + 1

	#	for j in range(1,interval):
	#		y = cloud[i] + (cloud[z] - cloud[i]) / interval * j
	#		cloud_interpol.append(y)

	#	cloud_interpol.append(cloud[z])

	#cloud_interpol = cloud_interpol[12:]
	#cloud_interpol.append([0]*23)

	#################################################################################################################################

	forecastPV = [(beta3*(x**3) + beta2*(x**2) + beta1*x) for x in ghi_API_interpol]

	return(forecastPV)


#def forecastxxx(date_from_DB):
#	db = sqlite3.connect(config.dbfilepath)
#	cur = db.cursor()
#
#	cur.execute("SELECT * FROM solarLog WHERE datetime LIKE ?", (date_from_DB+'%' ,))
#	data = cur.fetchall()
#
#	solar = list(zip(*data)[1])
#	solar = [x*100 for x in solar]
#	addsolar = [0]*12
#	solar = addsolar + solar
#	return(solar)

