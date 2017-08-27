#!/usr/bin/env python
#Version 1.2
import sys
sys.path.append('/var/www/html/modules/libraries')
import paho.mqtt.client as mqtt
import mysql.connector
import datetime
import time
import iRulez_logging as logger

file = open('/var/www/html/config.php', 'r')

for line in file:
    if "db_name" in line: MySQL_database = line.split('"')[3]
    elif "db_user" in line: MySQL_username = line.split('"')[3]
    elif "db_password" in line: MySQL_password = line.split('"')[3]

cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
cursor = cnx.cursor()
query = ("SELECT Setting,value FROM Settings")
cursor.execute(query)	
for (Setting, value) in cursor:
	if Setting == "MQTT_ip_address":
		MQTT_ip_address = value
	elif Setting == "MQTT_port_python":
		MQTT_port = value
cursor.close()
cnx.close()	
	
debug = "DEBUG"
info = "INFO"
alert = "INFO"


logger.printLog(info,"Auto config Started", str(logger.get_linenumber()))

def restart():			
		subprocess.call(["sudo", "supervisorctl", "restart" ,"AutoConfig"])  
		
def on_connect(mqttc, obj, rc):
	logger.printLog(debug,"rc: "+str(rc), str(logger.get_linenumber()))

def updateStatus(id):
	try:
		cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
		cursor = cnx.cursor()
		query = "UPDATE Core_Arduino_Outputs SET status = 'OFF' WHERE Core_Devices_id = " + str(id)
		logger.printLog(debug,"Query: " + query, str(logger.get_linenumber()))
		cursor.execute(query)
		cnx.commit()
	except Exception as e:
		logger.printLog(alert,e,str(logger.get_linenumber())) 
		raise
	finally:	
		cursor.close()
		cnx.close()	
		
def sendHostname():
	try:
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			query = ("SELECT MAC, nummer FROM Core_Devices")
			logger.printLog(debug,"Query: " + query, str(logger.get_linenumber()))
			cursor.execute(query)
			row = cursor.fetchone()
			while row is not None:
				logger.printLog(debug,"Publish: " + str(row[0]) + "/hostname/" + str(row[1]), str(logger.get_linenumber()))
				mqttc.publish(str(row[0]) + "/hostname",str(row[1]), 0, False)
				row = cursor.fetchone()	
	except Exception as e:
		logger.printLog(alert,e, str(logger.get_linenumber())) 
		raise
	finally:	
		cursor.close()
		cnx.close()	
	
def on_message(mqttc, obj, msg):
	logger.printLog(debug,"Received message: " + str(msg.topic) + "/" + str(msg.payload), str(logger.get_linenumber()))
	if "/ip" in msg.topic:
		try:
			MAC,action = msg.topic.split("/")
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			query = ("SELECT nummer FROM Core_Devices WHERE MAC = '" + str(MAC) + "'")
			logger.printLog(debug,"Query: " + query, str(logger.get_linenumber()))
			cursor.execute(query)
			row = cursor.fetchone()
			while row is not None:
				logger.printLog(debug,"Publish: " + str(MAC) + "/hostname/" + str(row[0]), str(logger.get_linenumber()))
				mqttc.publish(str(MAC) + "/hostname",str(row[0]), 0, False)
				row = cursor.fetchone()	
		except Exception as e:
			logger.printLog(alert,e, str(logger.get_linenumber())) 
			raise
		finally:	
			cursor.close()
			cnx.close()	
	elif "/lastWill" in msg.topic:
		try:
			MAC,action = msg.topic.split("/")
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			query = ("SELECT id, Nummer FROM Core_Devices WHERE MAC = '" + str(MAC) +"'")
			logger.printLog(debug,"Query: " + query, str(logger.get_linenumber()))
			cursor.execute(query)
			result=cursor.fetchone()
			updateStatus(result[0])
			
			topic = "FBL/checkStatus"
			payload =""
			logger.printLog(debug,"Publish: " + str(topic) +":"+ str(payload) , str(logger.get_linenumber()) )
			mqttc.publish(topic,payload, 0, False)	
			
			topic = "Telegram/Message"
			payload = "[ALERT] - Device " + result[1] + " with MAC: " + str(MAC) + " DOWN!"
			logger.printLog(debug,"Publish: " + topic +":"+ payload , str(logger.get_linenumber()) )
			mqttc.publish(topic,payload, 0, False)	
		except Exception as e:
			logger.printLog(alert,e, str(logger.get_linenumber()))
			raise
		finally:	
			cursor.close()
			cnx.close()	


def on_subscribe(mqttc, obj, mid, granted_qos):
	logger.printLog(debug,"Subscribed: "+str(mid)+" "+str(granted_qos), str(logger.get_linenumber()))

def on_disconnect(client, userdata, rc):
	logger.printLog(info, "on_disconnect!", str(logger.get_linenumber()))
	exit()

def on_log(mqttc, obj, level, string):
    logger.printLog(debug,string, str(logger.get_linenumber()))	
	

	
mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
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
		logger.printLog(info,"SLEEP", str(logger.get_linenumber())) 
		time.sleep(5)


logger.printLog(info,"Connected", str(logger.get_linenumber()))
sendHostname()

cnx = mysql.connector.connect(user=MySQL_username,charset='utf8',password=MySQL_password,database=MySQL_database)
cursor = cnx.cursor()
query = ("SELECT MAC FROM Core_Devices WHERE Arduino_Type != 4")
cursor.execute(query)

for (MAC) in cursor:
	logger.printLog(debug,"Subcribe: " + str(MAC[0]) +"/ip", str(logger.get_linenumber()))
	mqttc.subscribe(str(MAC[0]) +"/ip", 0)
	logger.printLog(debug,"Subcribe: " + str(MAC[0]) +"/lastWill", str(logger.get_linenumber()))
	mqttc.subscribe(str(MAC[0]) +"/lastWill", 0)
	
cursor.close()
cnx.close()	

try:
	cnx = mysql.connector.connect(user=MySQL_username,charset='utf8',password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	query = ("SELECT id, ShortName FROM html_Radio_zenders")
	cursor.execute(query)
	for (id, ShortName) in cursor:
		logger.printLog(debug,"Publish: radiolist/" + str(id) + "|" + str(ShortName), str(logger.get_linenumber()))
		mqttc.publish("radiolist",str(id) + "|" + str(ShortName), 0, True)
except Exception as e:
	logger.printLog(alert,e, str(logger.get_linenumber()))
	raise
finally:	
	cursor.close()
	cnx.close()


while True:
         mqttc.loop()