##########################
# 		Config file 	 #
##########################

import platform

if platform.system() == "Linux":
	dbfilepath = "/home/pi/pvmonitor-db/power.db"
	webserver = "Raspberry"
else:
	dbfilepath = "/Users/Martin/Desktop/meter/firmware hoelzl/power.db"
	webserver = "MacOSX"