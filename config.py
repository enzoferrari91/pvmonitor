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
    dbfilepath = "/Users/Martin/Desktop/pvmonitor/pvmonitor/testdb/power.db"
    apifilepath = "/Users/Martin/Desktop/pvmonitor/planetosAPI.txt"
    alarmfilepath = "/Users/Martin/Desktop/pvmonitor/alarm.txt"
    webserver = "MacOSX"

# Zwettl
lat = 48.50
lon = 15.25



# TEST SET - ERASE SOON...
##########################################################
activity  = {
    "xData": ["2016-11-01", "2016-11-02", "2016-11-03"],
    "datasets": [{
        "name": "Speed",
        "data": [20,12.524,11.441],
        "unit": "km/h",
        "type": "line",
        "valueDecimals": 1
    }, {
        "name": "Elevation",
        "data": [26.857,27,27.111],
        "unit": "m",
        "type": "area",
        "valueDecimals": 0
    }, {
        "name": "Heart rate",
        "data": [101,0,103],
        "unit": "bpm",
        "type": "area",
        "valueDecimals": 0
    }]
}
##########################################################