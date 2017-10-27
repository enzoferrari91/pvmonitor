import sqlite3
import config

def interpol_gfs(data,interval):
	length = len(data)
	data_interpol = list()
	data_interpol.append(data[0])

	for i in range(0,length-1):

		z = i + 1

		for j in range(1,interval):
			y = data[i] + (data[z] - data[i]) / interval * j
			data_interpol.append(y)

		data_interpol.append(data[z])

	data_interpol = data_interpol[12:]
	data_interpol.extend([0]*23)
	return(data_interpol)


def forecast(date_from_DB):
	interval = 12
	calc_with_GFS = False

	# +++ Forecast coefficients +++ #
	beta3 = -8.2e-6
	beta2 = 0.013
	beta1 = -0.09

	db = sqlite3.connect(config.dbfilepath)
	cur = db.cursor()

	try:
		cur.execute("SELECT * FROM forecastLogAPI WHERE datetime LIKE ?", (date_from_DB+'%' ,))
		data = cur.fetchall()

		ghi_API = list(zip(*data)[1])


		db.close()

		length = len(ghi_API)

		if length == 8:
			interval = 36
			ghi_API_interpol = list()
			ghi_API_interpol.extend([0]*24)
			ghi_API_interpol.append(ghi_API[0])

			for i in range(0,length-1):

				z = i + 1

				for j in range(1,interval):
					y = ghi_API[i] + (ghi_API[z] - ghi_API[i]) / interval * j
					ghi_API_interpol.append(y)

				ghi_API_interpol.append(ghi_API[z])

			ghi_API_interpol.extend([0]*11)

		if length == 24:
			ghi_API_interpol = list()
			ghi_API_interpol.append(ghi_API[0])

			for i in range(0,length-1):

				z = i + 1

				for j in range(1,interval):
					y = ghi_API[i] + (ghi_API[z] - ghi_API[i]) / interval * j
					ghi_API_interpol.append(y)

				ghi_API_interpol.append(ghi_API[z])

			ghi_API_interpol.extend([0]*11)
			
		forecastPV = [(beta3*(x**3) + beta2*(x**2) + beta1*x) for x in ghi_API_interpol]

	except:
		ghi_API_interpol = []
		calc_with_GFS = True

	#################################################################################################################################

	try:
		db = sqlite3.connect(config.dbfilepath)
		cur = db.cursor()

		cur.execute("SELECT * FROM forecastLog WHERE datetime LIKE ?", (date_from_DB+'%' ,))
		data = cur.fetchall()

		# 1 for cloud / 5 for ghi
		cloud = list(zip(*data)[1])
		temp = list(zip(*data)[2])
		temp = [x-273.15 for x in temp]

		ghi = list(zip(*data)[5])

		db.close()

		cloud_interpol = interpol_gfs(cloud,12)
		temp_interpol = interpol_gfs(temp,12)
		ghi_interpol = interpol_gfs(ghi,12)

		if calc_with_GFS==True:
			forecastPV = [(beta3*(x**3) + beta2*(x**2) + beta1*x) for x in ghi_interpol]

	except:
		cloud_interpol = []
		temp_interpol = []
		ghi_interpol = []
		forecastPV = []

	#################################################################################################################################
	return(forecastPV,ghi_API_interpol,cloud_interpol,temp_interpol,ghi_interpol)


forecast("2017-06-02")


