import sqlite3
import config

def forecast(date_from_DB):
	interval = 36

	# +++ Forecast coefficients +++ #
	beta = 5.2


	db = sqlite3.connect(config.dbfilepath)
	cur = db.cursor()

	cur.execute("SELECT * FROM forecastLogAPI WHERE datetime LIKE ?", (date_from_DB+'%' ,))
	data = cur.fetchall()

	ghi_API = list(zip(*data)[1])

	db.close()

	length = len(ghi_API)
	ghi_API_interpol = list()
	ghi_API_interpol.extend([0]*11)
	ghi_API_interpol.append(ghi_API[0])

	for i in range(0,length-1):

		z = i + 1

		for j in range(1,interval):
			y = ghi_API[i] + (ghi_API[z] - ghi_API[i]) / interval * j
			ghi_API_interpol.append(y)

		ghi_API_interpol.append(ghi_API[z])

	ghi_API_interpol.extend([0]*24)

	forecastPV = [beta * ghi for ghi in ghi_API_interpol]

	return(forecastPV)




