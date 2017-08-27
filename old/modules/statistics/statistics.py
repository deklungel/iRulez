#!/usr/bin/env python
#Version 1.2
import sys
sys.path.append('/var/www/html/modules/libraries')
import paho.mqtt.client as mqtt
import mysql.connector
import datetime
import time
from inspect import currentframe

file = open('/var/www/html/config.php', 'r')

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
		if Setting == "MQTT_ip_address":
			MQTT_ip_address = value
		elif Setting == "MQTT_port_python":
			MQTT_port = int(value)
		elif Setting == "loglevel":
			Loglevel = value
except Exception as e:
		printLog(info,e,str(get_linenumber())) 
finally:	
	cursor.close()
	cnx.close()	
	
debug = "DEBUG"
info = "INFO"
	
def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno
	
def printLog(level,message,Line):
	if (level.upper() == Loglevel.upper() or (level.upper() == info.upper() and Loglevel.upper() == debug.upper())):
		if(Loglevel.upper() == debug.upper()):
			strLine = " Line: "+Line
		else:
			strLine = ""
		print(level +"["+str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + "]"+strLine+" : " +str(message))

		
def get_id_Core_Arduino_Output(Arduino,Relais):
	try:
		cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
		cursor = cnx.cursor()
		query = ("SELECT id FROM Core_Arduino_Outputs WHERE arduino = "+str(Arduino)+" AND pin = "+str(Relais))
		cursor.execute(query)
		result=cursor.fetchone()
		if result is None:
			return ""
		else:
			return result[0]
	except Exception as e:
		printLog(info,e,str(get_linenumber())) 
	finally:	
		cursor.close()
		cnx.close()	
	
		

def get_H_Time(id_Core_Arduino_Output):
	try:
		cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
		cursor = cnx.cursor()
		printLog(debug,"id_Core_Arduino_Output: "+str(id_Core_Arduino_Output), str(get_linenumber()))
		query = ("SELECT id, Time_on FROM Core_Stats WHERE id_Core_Arduino_Output = "+str(id_Core_Arduino_Output)+" AND time_delta IS NULL")
		printLog(debug, query, str(get_linenumber()))
		cursor.execute(query)
		result=cursor.fetchone()
		if result is None:
			return ""
		else:
			return result
	except Exception as e:
		printLog(info,e,str(get_linenumber())) 
	finally:	
		cursor.close()
		cnx.close()	
		

def on_connect(mqttc, obj, rc):
	printLog(info,"rc: "+str(rc), str(get_linenumber()))

def on_message(mqttc, obj, msg):
	printLog(debug, msg.topic + "/" + msg.payload, str(get_linenumber()))
	if msg.topic == "StatsService/service/cleanup":
		try:
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			query = ("DELETE FROM Core_Stats WHERE Time_on < DATE_SUB(CURDATE(), INTERVAL 1 YEAR)")
			printLog(debug, query, str(get_linenumber()))
			cursor.execute(query)
			cnx.commit()
			query = ("DELETE FROM Core_Stats WHERE time_delta < 1")
			printLog(debug, query, str(get_linenumber()))
			cursor.execute(query)
			cnx.commit()
			printLog(info, "Cleanup of database has been executed", str(get_linenumber()))
			
			query = ("SELECT id, DatesON FROM Core_Stats WHERE time_delta IS NULL")
			cursor.execute(query)
			for (id, DatesON) in cursor:
				try:
					cnx2 = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
					cursor2 = cnx2.cursor()
					Time = datetime.datetime.now()
					if DatesON != "":
						DatesON = DatesON+"|"
					DatesONAdj = DatesON+Time.strftime("%Y-%m-%d")
					printLog(info,"UPDATE Core_Stats SET DatesON = '"+ str(DatesONAdj) +"' WHERE id= "+str(id), str(get_linenumber()))
					query = ("UPDATE Core_Stats SET DatesON = '"+ str(DatesONAdj) +"' WHERE id= "+str(id))
					cursor2.execute(query)
					cnx2.commit()
				except Exception as e:
					printLog(info,e,str(get_linenumber())) 
				finally:	
					cursor2.close()
					cnx2.close()	
		except Exception as e:
			printLog(info,e,str(get_linenumber())) 
		finally:	
			cursor.close()
			cnx.close()	
		
		
	else:
		if msg.payload == "H":
			tmpArduino,tmpRelais,status = msg.topic.split("/")
			Arduino = tmpArduino.replace("arduino", "")
			Relais = tmpRelais.replace("relais", "")
			Time = datetime.datetime.now()

			id_Core_Arduino_Output = get_id_Core_Arduino_Output(Arduino,Relais)
			printLog(info, "id_Core_Arduino_Output: "+str(id_Core_Arduino_Output), str(get_linenumber()))
			if id_Core_Arduino_Output != "":
				try:
					Time_on = get_H_Time(id_Core_Arduino_Output)
					cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
					cursor = cnx.cursor()
					if Time_on != "":
						query = ("DELETE FROM Core_Stats WHERE id_Core_Arduino_Output = "+str(id_Core_Arduino_Output)+" AND time_delta IS NULL")
						printLog(debug, query, str(get_linenumber()))
						cursor.execute(query)
						cnx.commit()
					query = ("INSERT INTO Core_Stats (id_Core_Arduino_Output, Time_on, DatesON) VALUES (%s, %s, %s)")
					printLog(debug, "INSERT INTO Core_Stats (id_Core_Arduino_Output, Time_on, DatesON) VALUES ("+str(id_Core_Arduino_Output)+","+str(Time)+","+str(Time.strftime("%d/%m"))+")", str(get_linenumber()))
					data = (id_Core_Arduino_Output, Time, Time.strftime("%Y-%m-%d"))
					cursor.execute(query,data)
					cnx.commit()	
				except Exception as e:
					printLog(info,e,str(get_linenumber())) 
				finally:	
					cursor.close()
					cnx.close()	
			else:
				printLog(info, "No Arduino Output ID found for Arduino: " +str(Arduino)+ " and Relais "+str(Relais), str(get_linenumber()))
		else:
			tmpArduino,tmpRelais,status = msg.topic.split("/")
			Arduino = tmpArduino.replace("arduino", "")
			Relais = tmpRelais.replace("relais", "")
			Time = datetime.datetime.now()
		
			id_Core_Arduino_Output = get_id_Core_Arduino_Output(Arduino,Relais)
			if id_Core_Arduino_Output != "":
				stat = get_H_Time(id_Core_Arduino_Output)
				if stat != "":
					id = stat[0]
					Time_on = stat[1]
					time_delta = (Time - Time_on).total_seconds()
					try:
						cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
						cursor = cnx.cursor()
						query = ("UPDATE Core_Stats SET time_delta = "+ str(time_delta) +", Time_off = '"+str(Time)+"' WHERE id= "+str(id))
						printLog(debug,"UPDATE Core_Stats SET time_delta = "+ str(time_delta) +", Time_off = '"+str(Time)+"' WHERE id= "+str(id), str(get_linenumber()))
						cursor.execute(query)
						cnx.commit()
					except Exception as e:
						printLog(info,e,str(get_linenumber())) 
					finally:	
						cursor.close()
						cnx.close()	
				else:
					printLog(info, "No Relais H found for Arduino Output ID: " +str(id_Core_Arduino_Output), str(get_linenumber()))
			else:
				printLog(info, "No Arduino Output ID found for Arduino: " +str(Arduino)+ " and Relais "+str(Relais), str(get_linenumber()))
			
def on_subscribe(mqttc, obj, mid, granted_qos):
	printLog(info,"Subscribed: "+str(mid)+" "+str(granted_qos), str(get_linenumber()))

def on_log(mqttc, obj, level, string):
    printLog(info,string, str(get_linenumber()))	
	
def on_disconnect(client, userdata, rc):
	printLog(info, "on_disconnect!", str(get_linenumber()))
	exit()	

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect
# Uncomment to enable debug messages
#mqttc.on_log = on_log	
	
printLog(info,"Connecting", str(get_linenumber()))	
running = True
while running:
	try:
		mqttc.connect(MQTT_ip_address,int(MQTT_port), 60)
		running = False
	except:
		printLog(info,"Sleep", str(get_linenumber()))
		time.sleep(5)
printLog(info,"Connected", str(get_linenumber()))
try:
	cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	query = ("SELECT arduino, pin FROM Core_Arduino_Outputs WHERE monitor = 1")
	cursor.execute(query)

	for (arduino) in cursor:
		printLog(info,"arduino" + str(arduino[0]) +"/relais" + str(arduino[1]) + "/status", str(get_linenumber()))
		mqttc.subscribe("arduino" + str(arduino[0]) +"/relais" + str(arduino[1]) + "/status", 0)
		
except Exception as e:
	printLog(info,e,str(get_linenumber())) 
finally:	
	cursor.close()
	cnx.close()	

mqttc.subscribe("StatsService/service/cleanup", 0)

while True:
 mqttc.loop()
