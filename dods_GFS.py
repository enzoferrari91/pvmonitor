import requests
import re
from datetime import datetime
from datetime import timedelta

today = datetime.today()
yesterday = today - timedelta(days=1)
sDate = str(yesterday.year) + str(yesterday.month) + str(yesterday.day)

print("Forecast date: " + sDate)

variables = ["dswrfsfc","tmp2m"]

out=list()

for v in variables:
	print(v)
	url = ("http://nomads.ncep.noaa.gov:9090/dods/gfs_0p25/gfs" + sDate + "/gfs_0p25_12z.ascii?" + v + "[1:20][552:552][60:60]")
	r = requests.get(url)
	data = r.text
	end = data.index("time")
	data = data[0:end]
	data = str(data)
	data = data.replace("\n","")
	data = data.replace(" ","")
	data = re.sub("[\(\[].*?[\)\]]","",data)
	datalist = data.split(",")
	datalist = datalist[2:10]
	datalist = [float(x) for x in datalist]
	out.append(datalist)

dataDB = zip(*out)