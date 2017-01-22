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
	ghi_API_interpol.extend([0]*12)
	ghi_API_interpol.append(ghi_API[0])

	for i in range(0,length-1):

		z = i + 1

		for j in range(1,interval):
			y = ghi_API[i] + (ghi_API[z] - ghi_API[i]) / interval * j
			ghi_API_interpol.append(y)

		ghi_API_interpol.append(ghi_API[z])

	ghi_API_interpol.extend([0]*23)

	forecastPV = [beta * ghi for ghi in ghi_API_interpol]

	# +++ Time correction table +++ #
	time_correct = list()
	time_correct.extend([0]*12*7) # 0-7
	time_correct.extend([1]*12*1) # 7-8
	time_correct.extend([1.2]*12*1) # 8-9
	time_correct.extend([1.5]*12*1) # 9-10
	time_correct.extend([2]*12*1) # 10-11
	time_correct.extend([2.2]*12*1) # 11-12
	time_correct.extend([2.1]*12*1) # 12-13
	time_correct.extend([2.2]*12*1) # 13-14
	time_correct.extend([2.5]*12*1) # 14-15
	time_correct.extend([2]*12*1) # 15-16
	time_correct.extend([1]*12*3) # 16-19
	time_correct.extend([0]*12*5) # 19-24

	for i in range(0,len(forecastPV)):
		forecastPV[i] = forecastPV[i] * time_correct[i]


	return(forecastPV)




