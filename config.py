##########################
# Config file
##########################

import platform

if platform.system() == "Linux":
    dbfilepath = "/home/pi/pvmonitor-db/power.db"
    apifilepath = "/home/pi/planetosAPI.txt"
    zstfilepath = "/home/pi/tempzst.txt"
    alarmfilepath = "/home/pi/alarm.txt"
    logfilepath = "/home/pi/pvmonitor-logs/"
    webserver = "Raspberry"
else:
    dbfilepath = "/Users/martinlenz/Desktop/Python/pvmonitor/pvmonitor/testdb/power.db"
    apifilepath = "/Users/martinlenz/Desktop/Python/pvmonitor/planetosAPI.txt"
    alarmfilepath = "/Users/martinlenz/Desktop/Python/pvmonitor/alarm.txt"
    webserver = "MacOSX"

# Zwettl
lat = 48.50
lon = 15.25
