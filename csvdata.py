from datetime import datetime
from datetime import timedelta
import sqlite3
import csv
import config

def extractdate(s):
	end = s.index(" ")
	return s[:end]

def selectDB(date_from_DB, date_to_DB):
	db = sqlite3.connect(config.dbfilepath)
	cur = db.cursor()

	cur.execute("SELECT * FROM powerLog WHERE datetime >= ? and datetime <= ?", (date_from_DB, date_to_DB))
	data = cur.fetchall()

	# Create lists
	power_pv = list(zip(*data)[3])
	timestampList = list(zip(*data)[0])
	timestampList = [str(x) for x in timestampList]

	cur.execute("SELECT * FROM forecastLog WHERE datetime >= ? and datetime <= ?", (date_from_DB, date_to_DB))
	data = cur.fetchall()

	# data[0]...timestamps
	# data[1]...cloud cover
	# data[2]...temperature
	# data[3]...u-wind
	# data[4]...v-wind
	# data[5]...ghi

	cloud = list(zip(*data))[1]
	temperature = list(zip(*data))[2]
	ghi = list(zip(*data)[5])
	timestampList_fcast = list(zip(*data)[0])
	timestampList_fcast = [str(x) for x in timestampList_fcast]

	cur.execute("SELECT * FROM forecastLogAPI WHERE datetime >= ? and datetime <= ?", (date_from_DB, date_to_DB))
	data = cur.fetchall()

	ghi_API = list(zip(*data)[1])
	timestampList_fcast_API = list(zip(*data)[0])
	timestampList_fcast_API = [str(x) for x in timestampList_fcast_API]

	
	db.close()

	# Return the lists
	return (power_pv, timestampList, cloud, temperature, ghi, timestampList_fcast, ghi_API, timestampList_fcast_API)


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

	#return(csv)
	return(output)

power_pv, timestampList, cloud, temperature, ghi, timestampList_fcast, ghi_API, timestampList_fcast_API = selectDB("2017-01-03 01:00","2017-06-02 22:05")

print "start interpol"

csvfcastCLOUD = interpol(cloud, timestampList_fcast,12)
csvfcastTEMPERATURE = interpol(temperature, timestampList_fcast,12)
csvfcastGHI = interpol(ghi, timestampList_fcast,12)
csvfcastAPI = interpol(ghi_API,timestampList_fcast_API,36)


outpv = list()

timestampList = [x[:16] for x in timestampList]

outpv.append(timestampList)
outpv.append(power_pv)
csvpv = zip(*outpv)

print "start sync"


def sync_lists(list_one, list_two,numb):
	temp_list_one = list()
	temp_list_two = list()

	temp_list_two_two = list()
	temp_list_two_three = list()
	temp_list_two_four = list()

	timelist = list()
	output = list()

	y=0
	length = len(list_one[0])
	ll = len(list_two[0])

	 
	for i in range(0,length):
		if not list_one[0][i] == list_two[0][y]:
			check = 0

			while check == 0:
				y = y + 1
				if y == ll:
					break

				if list_one[0][i] == list_two[0][y]:
					check = 1

		if not y == ll:
			timelist.append(list_one[0][i])
			temp_list_one.append(list_one[1][i])
			temp_list_two.append(list_two[1][y])

			if numb == 2:
				temp_list_two_two.append(list_two[2][y])

			if numb	== 3:
				temp_list_two_two.append(list_two[2][y])
				temp_list_two_three.append(list_two[3][y])

			if numb == 4:
				temp_list_two_two.append(list_two[2][y])
				temp_list_two_three.append(list_two[3][y])
				temp_list_two_four.append(list_two[4][y])

			y = y + 1

		if y == ll:
			y = 0

	output.append(timelist)
	output.append(temp_list_one)
	output.append(temp_list_two)
	
	if numb == 2:
		output.append(temp_list_two_two)
	if numb == 3:
		output.append(temp_list_two_two)
		output.append(temp_list_two_three)
	if numb == 4:
		output.append(temp_list_two_two)
		output.append(temp_list_two_three)
		output.append(temp_list_two_four)

	return(output)

print "1"
output_first = sync_lists(csvfcastCLOUD,outpv,1)
print "2"
output_second = sync_lists(csvfcastTEMPERATURE,output_first,2)
print "3"
output_third = sync_lists(csvfcastGHI,output_second,3)
print "4"
output_fourth = sync_lists(csvfcastAPI,output_third,4)

csvlist = zip(*output_fourth)

with open("pv.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(csvlist)




















