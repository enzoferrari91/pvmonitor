import requests

url = "http://nomads.ncep.noaa.gov:9090/dods/gfs_0p25/gfs20161116/gfs_0p25_12z.ascii?dswrfsfc[1:20][550:550][60:61]"

print "Start"
r = requests.get(url)
print(r.text)