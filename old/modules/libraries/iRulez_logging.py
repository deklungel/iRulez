#!/usr/bin/env python
import sys
import time
import pprint
import datetime
from inspect import currentframe
import mysql.connector
file = open('/var/www/html/config.php', 'r')

debug = "DEBUG"
info = "INFO"
alert = "ALERT"

for line in file:
	if "db_name" in line: MySQL_database = line.split('"')[3]
	elif "db_user" in line: MySQL_username = line.split('"')[3]
	elif "db_password" in line: MySQL_password = line.split('"')[3]


	
try:	
	cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	query = ("SELECT Setting,value FROM Settings")
	cursor.execute(query)	
	for (Setting, value) in cursor:
		if Setting == "loglevel":
			Loglevel = value
except Exception as e:
	raise
finally:	
	cursor.close()
	cnx.close()	
	
def get_linenumber():
	try:
		cf = currentframe()
		return cf.f_back.f_lineno
	except Exception as e:
		raise
	finally:	
		cursor.close()
		cnx.close()	
	
def printLog(level,message,Line):
	try:	
		if ( level.upper() == Loglevel.upper() or (level.upper() == info.upper() and Loglevel.upper() == debug.upper()) or level.upper() == alert.upper() ):
			if(Loglevel.upper() == debug.upper()):
				strLine = " Line: "+Line
			else:
				strLine = ""
			print(level +"["+str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + "]"+strLine+" : " +str(message))
	except Exception as e:
		raise
	finally:	
		cursor.close()
		cnx.close()	