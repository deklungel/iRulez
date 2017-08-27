#!/usr/bin/env python
#Version 0.1

import sys
sys.path.append('/var/www/html/modules/libraries')
import mysql.connector
import paho.mqtt.client as mqtt
import datetime
import time
from inspect import currentframe
import iRulez_logging as logger

file = open('/var/www/html/config.php', 'r')

debug = "DEBUG"
info = "INFO"
alert = "ALERT"

logger.printLog(info,'**** FBL Started ****', str(logger.get_linenumber()))

for line in file:
	if "db_name" in line: MySQL_database = line.split('"')[3]
	elif "db_user" in line: MySQL_username = line.split('"')[3]
	elif "db_password" in line: MySQL_password = line.split('"')[3]

try:	
	cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	query = ("SELECT Setting,value FROM Settings")
	print("query: "+query)
	cursor.execute(query)	
	for (Setting, value) in cursor:
		if Setting == "MQTT_ip_address":
			MQTT_ip_address = value
		elif Setting == "MQTT_port_python":
			MQTT_port = value
except Exception as e:
	logger.printLog(alert,e, str(logger.get_linenumber()))
	raise
finally:		
	cursor.close()	
	cnx.close()
	

def updateStatus(Arduino,Relais,status):
	if (status == 'H'):
		status = 'ON'
		Time = "'"+str(datetime.datetime.now())+"'"
	else:
		status = 'OFF'
		Time = "NULL"
	cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	query = "UPDATE Core_Arduino_Outputs SET status = '"+str(status)+"', status_time = "+str(Time)+", notification_snooze = NULL, notification_dismiss = 0 WHERE arduino = " + str(Arduino) + " and pin = " + str(Relais)
	logger.printLog(debug,"Query: " + query, str(logger.get_linenumber()))
	cursor.execute(query)
	cnx.commit()
	cursor.close()
	cnx.close()	

def updateFBL_Status(id,status):
	cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	query = "UPDATE Core_vButtonDB SET FBL_Status = '"+status+"' WHERE id = "+str(id)
	logger.printLog(debug,"Query: " + query, str(logger.get_linenumber()))
	cursor.execute(query)
	cnx.commit()
	cursor.close()
	cnx.close()		

def PhysicalFBL(id,action):
	if (action == 'H'):
		status = 'ON'
	else:
		status = 'OFF'
	cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	query = "SELECT Core_Arduino_Outputs.arduino, Core_Arduino_Outputs.pin, Core_Arduino_Outputs.status FROM Core_vButtonDB_actions_FBL INNER JOIN Core_Arduino_Outputs ON Core_Arduino_Outputs.id = Core_vButtonDB_actions_FBL.Core_Arduino_Outputs_id WHERE Core_vButtonDB_id = " + str(id)
	cursor.execute(query)
	for (arduino,pin,Relais_status) in cursor:	
		 if(Relais_status !=  action ):
			mqttc.publish("arduino" + str(arduino) + "/relais" + str(pin) + "/action", str(action), 0, False)
		
def on_connect(mqttc, obj, rc):
	logger.printLog(debug,"rc: "+str(rc) , str(logger.get_linenumber()))

def on_message(mqttc, obj, msg):	
	if "/status" in msg.topic:
		logger.printLog(debug, "on_message: " + msg.topic + "/" + msg.payload  , str(logger.get_linenumber()))
		tmpArduino,tmpRelais,action = msg.topic.split("/")
		Arduino = tmpArduino.replace("arduino", "")
		Relais = tmpRelais.replace("relais", "")
		updateStatus(Arduino,Relais,msg.payload)
		CheckvButton()
	elif "/checkStatus" in msg.topic:
		CheckvButton()
	
	
def on_publish(mqttc, obj, mid):
	logger.printLog(debug,"Publish: "+str(mid), str(logger.get_linenumber()))
	
def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.printLog(debug,"Subscribed: "+str(mid)+" "+str(granted_qos) , str(logger.get_linenumber()))

def on_log(mqttc, obj, level, string):
    logger.printLog(debug,string , str(logger.get_linenumber()))	

def on_disconnect(client, userdata, rc):
	logger.printLog(info, "on_disconnect!", str(logger.get_linenumber()))
	exit()	
	
def CheckvButton():
	#check on every message
	logger.printLog(debug,"CheckvButton" , str(logger.get_linenumber()))
	try:
		cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
		cursor = cnx.cursor()
		query = "SELECT id,FBL,FBL_Status,arduino,pin FROM Core_vButtonDB WHERE FBL != 'NONE' "
		logger.printLog(debug,"Query: " + query, str(logger.get_linenumber()))
		cursor.execute(query)
		vButtonID = ''
		arr_id = []
		arr_vbutton = []
		arr_fbl = []
		arr_FBL_Status = []
		arr_ON_ON = []
		arr_ON_OFF = []
		arr_OFF_ON = []
		arr_OFF_OFF = []
		arr_Toggle_ON = []
		arr_Toggle_OFF = []
		counter = -1
		# for (id,arduino,pin,status,FBL,FBL_Status,type) in cursor:
		for (id,FBL,FBL_Status,arduino,pin) in cursor:

			arr_id.append(id)
			arr_vbutton.append("arduino"+str(arduino)+"/vbutton"+str(pin)+"/status")
			arr_fbl.append(FBL)
			arr_FBL_Status.append(FBL_Status)
			vButtonID = id
			counter = counter + 1
			arr_ON_ON.append(0)
			arr_ON_OFF.append(0)
			arr_OFF_ON.append(0)
			arr_OFF_OFF.append(0)
			arr_Toggle_ON.append(0)
			arr_Toggle_OFF.append(0)
				
			try:
				cnx2 = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
				cursor2 = cnx2.cursor()
				query = "SELECT id , type FROM Core_vButtonDB_actions WHERE action_nummer = 1 and core_vButtonDB_id = " + str(id)
				logger.printLog(debug,"Query: " + query, str(logger.get_linenumber()))
				cursor2.execute(query)
				for (id_Core_vButtonDB_actions , type) in cursor2:
					# Hierna nog aanpassen
					try:
						cnx3 = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
						cursor3 = cnx3.cursor()
						query = "SELECT Core_Arduino_Outputs.status FROM Core_vButtonDB_actions_Arduino INNER JOIN Core_Arduino_Outputs ON Core_Arduino_Outputs_id = Core_Arduino_Outputs.id WHERE Core_vButtonDB_actions_id = " + str(id_Core_vButtonDB_actions)
						logger.printLog(debug,"Query: " + query, str(logger.get_linenumber()))
						cursor3.execute(query)
						for (status) in cursor3:	
							if(type == 'T'):
								logger.printLog(debug, 'type: ' + str(type),str(logger.get_linenumber()))
								logger.printLog(debug, 'status: ' + str(status[0]),str(logger.get_linenumber()))
								if(status[0] == 'ON' ):
									arr_Toggle_ON[counter] = arr_Toggle_ON[counter] + 1
									logger.printLog(debug, 'Toggle_ON: ' + str(arr_Toggle_ON[counter]),str(logger.get_linenumber()))
								else:
									arr_Toggle_OFF[counter] = arr_Toggle_OFF[counter] + 1
									logger.printLog(debug, 'Toggle_OFF: ' + str(arr_Toggle_OFF[counter]),str(logger.get_linenumber()))
							elif(type == 'ON'):
								if(status[0] == 'ON' ):
									arr_ON_ON[counter] = arr_ON_ON[counter] + 1
									logger.printLog(debug, 'ON_ON: ' + str(arr_ON_ON[counter]),str(logger.get_linenumber()))
								else:
									arr_ON_OFF[counter] = arr_ON_OFF[counter] + 1
									logger.printLog(debug, 'ON_OFF: ' + str(arr_ON_OFF[counter]),str(logger.get_linenumber()))
							else:
								if(status[0] == 'ON' ):
									arr_OFF_ON[counter] = arr_OFF_ON[counter] + 1
									logger.printLog(debug, 'OFF_ON: ' + str(arr_OFF_ON[counter]),str(logger.get_linenumber()))
								else:
									arr_OFF_OFF[counter] = arr_OFF_OFF[counter] + 1
									logger.printLog(debug, 'OFF_OFF: ' + str(arr_OFF_OFF[counter]),str(logger.get_linenumber()))
					except Exception as e:
						logger.printLog(alert,e,str(logger.get_linenumber())) 
					finally:	
						cursor3.close()
						cnx3.close()	
			except Exception as e:
				logger.printLog(alert,e,str(logger.get_linenumber())) 
			finally:	
				cursor2.close()
				cnx2.close()	

		for i in range(len(arr_id)):
			if(arr_fbl[i] == 'FBL'):
				if(arr_Toggle_ON[i] > 0 or arr_ON_ON[i] > 0 or arr_OFF_ON[i] > 0):
					if(arr_FBL_Status[i] == "DOWN" ):
						mqttc.publish(arr_vbutton[i], "H", 0, True)
						updateFBL_Status(arr_id[i],"UP")
						PhysicalFBL(arr_id[i],'H')
				else:
					if(arr_FBL_Status[i] == "UP" ):
						mqttc.publish(arr_vbutton[i], "L", 0, True)
						PhysicalFBL(arr_id[i],'L')
						updateFBL_Status(arr_id[i],"DOWN")
			elif(arr_fbl[i] == 'RFBL' ):
				if(arr_Toggle_OFF[i] > 0 or arr_ON_OFF[i] > 0 or arr_OFF_OFF[i] > 0):
					if(arr_FBL_Status[i] == "DOWN" ):
						mqttc.publish(arr_vbutton[i], "H", 0, True)
						PhysicalFBL(arr_id[i],'H')
						updateFBL_Status(arr_id[i],"UP")
				else:
					if(arr_FBL_Status[i] == "UP" ):
						mqttc.publish(arr_vbutton[i], "L", 0, True)
						PhysicalFBL(arr_id[i],'L')
						updateFBL_Status(arr_id[i],"DOWN")
			elif(arr_fbl[i] == 'CFBL' ):
				if(arr_ON_OFF[i] > 0 or arr_OFF_ON[i] > 0 or arr_Toggle_OFF[i] > 0):
					if(arr_FBL_Status[i] == "UP" ):
						mqttc.publish(arr_vbutton[i], "L", 0, True)
						PhysicalFBL(arr_id[i],'L')
						updateFBL_Status(arr_id[i],"DOWN")
				else:
					if(arr_FBL_Status[i] == "DOWN" ):
						mqttc.publish(arr_vbutton[i], "H", 0, True)
						PhysicalFBL(arr_id[i],'H')
						updateFBL_Status(arr_id[i],"UP")
				
	except Exception as e:
		logger.printLog(alert,e,str(logger.get_linenumber())) 
	finally:	
		cursor.close()
		cnx.close()	
	
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect
# Uncomment to enable debug messages
#mqttc.on_log = on_log

running = True
while running:
	try:
		mqttc.connect(MQTT_ip_address,int(MQTT_port), 60)
		running = False
	except:
		logger.printLog(alert,"Sleep" , str(logger.get_linenumber()))
		time.sleep(5)

logger.printLog(info,"Connected" , str(logger.get_linenumber()))
mqttc.subscribe("FBL/checkStatus", 0)

for i in range(16):
	mqttc.subscribe("+/relais" + str(i) + "/status", 0)
	
while True:
	mqttc.loop()