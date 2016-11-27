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
	return (power_pv, timestampList, ghi, timestampList_fcast, ghi_API, timestampList_fcast_API)


power_pv, timestampList, ghi, timestampList_fcast, ghi_API, timestampList_fcast_API = selectDB("2016-11-21 00:00","2016-11-24 00:00")

print timestampList_fcast

def interpol(ghi, timestampList_fcast, interval,filename):
	# interval 12, 36
	length = len(ghi)

	listeghi = list()
	listetime = list()

	listeghi.append(ghi[0])
	listetime.append(timestampList_fcast[0])


	for i in range(0,length-1):

		z = i + 1

		for j in range(1,interval):
			y = ghi[i] + (ghi[z] - ghi[i]) / interval * j
			t = datetime.strptime(timestampList_fcast[i],"%Y-%m-%d %H:%M") + timedelta(minutes=5*j)
			t = datetime.strftime(t, "%Y-%m-%d %H:%M")
			listeghi.append(y)
			listetime.append(t)

		listeghi.append(ghi[z])
		listetime.append(timestampList_fcast[z])

	print("Ausgabe")
	print(listeghi)
	print(listetime)

	outfcast = list()

	outfcast.append(listetime)
	outfcast.append(listeghi)

	csvfcast = zip(*outfcast)
	print csvfcast
	return csvfcast

csvfcast = interpol(ghi, timestampList_fcast,12,"fcast.csv")
csvfcastAPI = interpol(ghi_API,timestampList_fcast_API,36,"fcastAPI.csv")

with open("outputfcast.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(csvfcast)
with open("outputfcastAPI.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(csvfcastAPI)



outpv = list()
outpv.append(timestampList)
outpv.append(power_pv)
csvpv = zip(*outpv)

with open("outputpv.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(csvpv)


