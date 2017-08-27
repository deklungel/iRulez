#!/usr/bin/env python
#Version 1.2
import sys
sys.path.append('/var/www/html/modules/libraries')
import paho.mqtt.client as mqtt
import mysql.connector
import datetime
import time

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
	elif Setting == "loglevel":
		Loglevel = value
cursor.close()
cnx.close()	
	
debug = "DEBUG"
info = "INFO"

def printLog(level,message):
	if (level.upper() == Loglevel.upper() or (level.upper() == info.upper() and Loglevel.upper() == debug.upper())):
		print(level +"["+str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + "]: " +str(message))

printLog(info,"Logger Started")
		
def restart():			
		subprocess.call(["sudo", "supervisorctl", "restart" ,"Timer_v1"])  

def on_connect(mqttc, obj, rc):
	printLog(info,"rc: "+str(rc))

def on_message(mqttc, obj, msg):
	printLog(info,"Received message: " + msg.topic + "/" + msg.payload)
	
def on_subscribe(mqttc, obj, mid, granted_qos):
	printLog(info,"Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    printLog(debug,string)	
	
def on_disconnect(client, userdata, rc):
	logger.printLog(info, "on_disconnect!", str(logger.get_linenumber()))
	exit()	

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
		print ("Sleep")
		time.sleep(5)
printLog(info,"Connected")


mqttc.subscribe("#", 0)		
	



while True:
	mqttc.loop()