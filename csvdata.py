from datetime import datetime
from datetime import timedelta
import sqlite3
import csv
import config


def selectDB(date_from_DB, date_to_DB):
	db = sqlite3.connect(config.dbfilepath)
	cur = db.cursor()

	cur.execute("SELECT * FROM powerLog WHERE datetime >= ? and datetime < ?", (date_from_DB, date_to_DB))
	data = cur.fetchall()

	# Create lists
	power_pv = list(zip(*data)[3])
	timestampList = list(zip(*data)[0])
	timestampList = [str(x) for x in timestampList]

	cur.execute("SELECT * FROM forecastLog WHERE datetime >= ? and datetime < ?", (date_from_DB, date_to_DB))
	data = cur.fetchall()

	cloud = list(zip(*data))[1]
	ghi = list(zip(*data)[5])
	timestampList_fcast = list(zip(*data)[0])
	timestampList_fcast = [str(x) for x in timestampList_fcast]

	cur.execute("SELECT * FROM forecastLogAPI WHERE datetime >= ? and datetime < ?", (date_from_DB, date_to_DB))
	data = cur.fetchall()

	ghi_API = list(zip(*data)[1])
	timestampList_fcast_API = list(zip(*data)[0])
	timestampList_fcast_API = [str(x) for x in timestampList_fcast_API]

	
	db.close()

	# Return the lists
	return (power_pv, timestampList, cloud, ghi, timestampList_fcast, ghi_API, timestampList_fcast_API)


def interpol(tseries, timestamps, interval):
	# interval 12, 36
	length = len(tseries)

	timestamps_interpol = list()
	tseries_interpol = list()
	output = list()

	timestamps_interpol.append(timestamps[0])
	tseries_interpol.append(tseries[0])

	for i in range(0,length-1):

		z = i + 1

		for j in range(1,interval):
			y = tseries[i] + (tseries[z] - tseries[i]) / interval * j
			t = datetime.strptime(timestamps[i],"%Y-%m-%d %H:%M") + timedelta(minutes=5*j)
			t = datetime.strftime(t, "%Y-%m-%d %H:%M")
			tseries_interpol.append(y)
			timestamps_interpol.append(t)

		tseries_interpol.append(tseries[z])
		timestamps_interpol.append(timestamps[z])

	output.append(timestamps_interpol)
	output.append(tseries_interpol)
	csv = zip(*output)

	return(csv)


power_pv, timestampList, cloud, ghi, timestampList_fcast, ghi_API, timestampList_fcast_API = selectDB("2017-01-15","2017-01-22")

csvfcastCLOUD = interpol(cloud, timestampList_fcast,12)
csvfcastGHI = interpol(ghi, timestampList_fcast,12)
csvfcastAPI = interpol(ghi_API,timestampList_fcast_API,36)

with open("fcastCLOUD.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(csvfcastCLOUD)

with open("fcastGHI.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(csvfcastGHI)

with open("fcastAPI.csv", "wb") as f:
	writer = csv.writer(f)
	writer.writerows(csvfcastAPI)

outpv = list()
outpv.append(timestampList)
outpv.append(power_pv)
csvpv = zip(*outpv)

with open("pv.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(csvpv)


