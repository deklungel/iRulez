#!/usr/bin/env python
import sys
sys.path.append('/var/www/html/modules/libraries')
import subprocess
import os
import time
import paho.mqtt.publish as publish
import mysql.connector

port = 1883
sendTelgram = False


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
	if Setting == "loglevel":
		Loglevel = value
	elif Setting == "MQTT_ip_address":
		MQTT_ip_address = value
	elif Setting == "MQTT_port_python":
		MQTT_port = int(value)
		
cursor.close()
cnx.close()	


while True:
	cat = subprocess.Popen(['ss','-ln','src',':'+str(port)], 
							stdout=subprocess.PIPE,
							)

	grep = subprocess.Popen(['grep', '-Ec','-e','\<'+str(port)+'\>'],
							stdin=cat.stdout,
							stdout=subprocess.PIPE,
							)

	end_of_pipe = grep.stdout

	for line in end_of_pipe:
		result = line.strip()
		
	if (int(result)  == 0):
		print 'Service Down'
		sendTelgram = True
		os.popen("service mosquitto stop", 'w')
		time.sleep(5)
		os.popen("service mosquitto start", 'w')
		time.sleep(5)
	elif(sendTelgram):
		time.sleep(10)
		publish.single( "Telegram/Message","!!! MQTT Service DOWN !!!", hostname=MQTT_ip_address,  port=MQTT_port,retain=False)
		sendTelgram = False
	
	time.sleep(10)