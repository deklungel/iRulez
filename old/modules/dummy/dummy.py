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

printLog(info,"Dummy Started")
		
def restart():			
		subprocess.call(["sudo", "supervisorctl", "restart" ,"Timer_v1"])  

def on_connect(mqttc, obj, rc):
	printLog(info,"rc: "+str(rc))

def on_message(mqttc, obj, msg):
	printLog(info,"Received message: " + msg.topic + "/" + msg.payload)
	if "/action" in msg.topic:
		tmpArduino,tmpRelais,action = msg.topic.split("/")
		Arduino = tmpArduino.replace("arduino", "")
		Relais = tmpRelais.replace("relais", "")
		if int(Relais) < 10:
			printLog(info,"Publish arduino" + str(Arduino) +"/dimmer" + str(Relais) + "/status/-1")
			mqttc.publish("arduino" + str(Arduino) +"/dimmer" + str(Relais) + "/status","-1", 0, True)
			if  str(msg.payload) == 'H':
				dimmerValue = 255
			else:
				dimmerValue = 0
			printLog(info,"Publish: WebInterface/arduino" + str(Arduino) +"/dimmer" + str(Relais) + "/status/" + str(dimmerValue))
			mqttc.publish("WebInterface/arduino" + str(Arduino) +"/dimmer" + str(Relais) + "/status",str(dimmerValue), 0, True)
					
		printLog(info,"Publish arduino" + str(Arduino) +"/relais" + str(Relais) + "/status/" + str(msg.payload))
		mqttc.publish("arduino" + str(Arduino) +"/relais" + str(Relais) + "/status",msg.payload, 0, True)
	elif "/dimmer" in msg.topic:
		tmpArduino,tmpRelais,action = msg.topic.split("/")
		Arduino = tmpArduino.replace("arduino", "")
		Relais = tmpRelais.replace("dimmer", "")
		DimmerTimer[int(Arduino)][int(Relais)] = int(time.time()) + 1
		DimmerStatus[int(Arduino)][int(Relais)] = int(msg.payload)
		value = "L"
		valueDimmer = 0
		if int(msg.payload) > 0:
			value = "H"
			valueDimmer = int(msg.payload)
			
		printLog(info,"Publish: WebInterface/arduino" + str(Arduino) +"/dimmer" + str(Relais) + "/status/" + str(valueDimmer))
		mqttc.publish("WebInterface/arduino" + str(Arduino) +"/dimmer" + str(Relais) + "/status",str(valueDimmer), 0, True)
							
		printLog(info,"Publish: arduino" + str(Arduino) +"/relais" + str(Relais) + "/status/" + str(value))
		mqttc.publish("arduino" + str(Arduino) +"/relais" + str(Relais) + "/status",value, 0, True)
	
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

cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
cursor = cnx.cursor()
query = ("SELECT arduino, pin FROM Core_Arduino_Outputs")
cursor.execute(query)

for (arduino,pin) in cursor:
	printLog(info,"arduino" + str(arduino) +"/relais" + str(pin) + "/action")
	mqttc.subscribe("arduino" + str(arduino) +"/relais" + str(pin) + "/action", 0)
	if pin < 10:
		printLog(info,"subscribe: arduino" + str(arduino) +"/dimmer" + str(pin) + "/value")
		mqttc.subscribe("arduino" + str(arduino) +"/dimmer" + str(pin) + "/value", 0)
	
query = ("SELECT arduino, pin FROM Core_vButtonDB")
cursor.execute(query)
for (arduino,pin) in cursor:
	printLog(info,"arduino" + str(arduino) +"/vbutton" + str(pin) + "/status")
	mqttc.subscribe("arduino" + str(arduino) +"/vbutton" + str(pin) + "/status", 0)
	
mqttc.subscribe("kodi0/#", 0)	
mqttc.subscribe("owntracks/#", 0)
mqttc.subscribe("clientMonitor/status/#", 0)
mqttc.subscribe("gateway/#", 0)
	
cursor.execute("SELECT count(DISTINCT arduino) FROM Core_vButtonDB")
result=cursor.fetchone()
number_of_arduino = result[0]
DimmerTimer = []
DimmerStatus = []
for i in xrange(number_of_arduino):
	DimmerTimer.append([])
	DimmerStatus.append([])
	for j in xrange(10):
		DimmerTimer[i].append(-1)
		DimmerStatus[i].append(-1)
	
cursor.close()
cnx.close()	


while True:
         mqttc.loop()
         for x in range (len(DimmerTimer)):
			for y in range (len(DimmerTimer[x])):
				if DimmerTimer[x][y] > -1 and int(time.time()) >= DimmerTimer[x][y]:
					Dimmervalue = DimmerStatus[x][y]
					if (DimmerStatus[x][y] == 0):
						Dimmervalue = -1
					printLog(info,"Publish: arduino" + str(x) +"/dimmer" + str(y) + "/status/" + str(Dimmervalue))
					mqttc.publish("arduino" + str(x) +"/dimmer" + str(y) + "/status",Dimmervalue, 0, True)
					
					
					# value = "L"
					# valueDimmer = 0
					# if DimmerStatus[x][y] > 0:
						# value = "H"
						# valueDimmer = DimmerStatus[x][y]
						
					# printLog(info,"Publish: WebInterface/arduino" + str(x) +"/dimmer" + str(y) + "/status/" + str(valueDimmer))
					# mqttc.publish("WebInterface/arduino" + str(x) +"/dimmer" + str(y) + "/status",str(valueDimmer), 0, True)
										
					# printLog(info,"Publish: arduino" + str(x) +"/relais" + str(y) + "/status/" + str(value))
					# mqttc.publish("arduino" + str(x) +"/relais" + str(y) + "/status",value, 0, True)
					DimmerStatus[x][y] = -1
					DimmerTimer[x][y] = -1

			