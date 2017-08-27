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
	elif Setting == "MonitorTimeout":
		TimeOut = value
cursor.close()
cnx.close()	
	
debug = "DEBUG"
info = "INFO"

def printLog(level,message):
	if (level.upper() == Loglevel.upper() or (level.upper() == info.upper() and Loglevel.upper() == debug.upper())):
		print(level +"["+str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + "]: " +str(message))

printLog(info,"Auto config Started")

def restart():			
		subprocess.call(["sudo", "supervisorctl", "restart" ,"Monitor"])  
		
def on_connect(mqttc, obj, rc):
	printLog(info,"rc: "+str(rc))

def on_message(mqttc, obj, msg):
	printLog(debug,"Received message: " + msg.topic + "/" + msg.payload)
	if "/ip" in msg.topic:
		try:
			MAC,action = msg.topic.split("/")
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			printLog(debug,"Query: UPDATE Core_Devices SET IP = '" + str(msg.payload) + "' WHERE MAC = '" + str(MAC) + "'")
			query = ("UPDATE Core_Devices SET IP = '" + str(msg.payload) + "' WHERE MAC = '" + str(MAC) + "'")
			cursor.execute(query)
			cnx.commit()
		except Error as e:
			print(e)
		finally:	
			cursor.close()
			cnx.close()
	if "/version" in msg.topic:
		try:
			MAC,action = msg.topic.split("/")
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			printLog(debug,"Query: UPDATE Core_Devices SET Versie = '" + str(msg.payload) + "' WHERE MAC = '" + str(MAC) + "'")
			query = ("UPDATE Core_Devices SET Versie = '" + str(msg.payload) + "' WHERE MAC = '" + str(MAC) + "'")
			cursor.execute(query)
			cnx.commit()
		except Error as e:
			print(e)
		finally:	
			cursor.close()
			cnx.close()
	if "/alive" in msg.topic:
		try:
			MAC,action = msg.topic.split("/")
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			printLog(debug,"Query: UPDATE Core_Devices SET MQTT = '0' WHERE MAC = '" + str(MAC) + "'")
			query = ("UPDATE Core_Devices SET MQTT = '0' WHERE MAC = '" + str(MAC) + "'")
			cursor.execute(query)
			cnx.commit()
		except Error as e:
			print(e)
		finally:	
			cursor.close()
			cnx.close()
	if "/type" in msg.topic:
		try:
			MAC,action = msg.topic.split("/")
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			printLog(debug,"Query: UPDATE Core_Devices SET Type = '" + str(msg.payload) + "' WHERE MAC = '" + str(MAC) + "'")
			query = ("UPDATE Core_Devices SET Type = '" + str(msg.payload) + "' WHERE MAC = '" + str(MAC) + "'")
			cursor.execute(query)
			cnx.commit()
		except Error as e:
			print(e)
		finally:	
			cursor.close()
			cnx.close()

def on_subscribe(mqttc, obj, mid, granted_qos):
	printLog(info,"Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    printLog(debug,string)	

def on_disconnect(client, userdata, rc):
	logger.printLog(info, "on_disconnect!", str(logger.get_linenumber()))
	exit()	
	
def ping(sHost):
	import subprocess
	try:
		output = subprocess.check_output("ping -c 1 "+sHost, shell=True)
	except Exception, e:
		return False
	return True
	
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

try:
	cnx = mysql.connector.connect(user=MySQL_username,charset='utf8',password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	query = ("SELECT MAC FROM Core_Devices")
	cursor.execute(query)
	# printLog(info,"Subcribe: DEADBEEFFEED/ip")
	# mqttc.subscribe("DEADBEEFFEED/ip", 0)
	# printLog(info,"Subcribe: DEADBEEFFEED/version")
	# mqttc.subscribe("DEADBEEFFEED/version", 0)
	# printLog(info,"Subcribe: DEADBEEFFEED/alive")
	# mqttc.subscribe("DEADBEEFFEED/alive", 0)
	# printLog(info,"Subcribe: DEADBEEFFEED/type")
	# mqttc.subscribe("DEADBEEFFEED/type", 0)
	for (MAC) in cursor:
		printLog(info,"Subcribe: " + str(MAC[0]) +"/ip")
		mqttc.subscribe(str(MAC[0]) +"/ip", 0)
		printLog(info,"Subcribe: " + str(MAC[0]) +"/version")
		mqttc.subscribe(str(MAC[0]) +"/version", 0)
		printLog(info,"Subcribe: " + str(MAC[0]) +"/alive ")
		mqttc.subscribe(str(MAC[0]) +"/alive", 0)
		printLog(info,"Subcribe: " + str(MAC[0]) +"/type ")
		mqttc.subscribe(str(MAC[0]) +"/type", 0)
	
	# printLog(debug,"Query: UPDATE Core_Devices SET IP = NULL, MQTT = 10, Ping = 10, Type = NULL, Versie = Null")
	# query = ("UPDATE Core_Devices SET IP = NULL, MQTT = 10, Ping = 10, Type = NULL, Versie = Null")
	# cursor.execute(query)
	# cnx.commit()
	
except Error as e:
	print(e)
finally:	
	cursor.close()
	cnx.close()	

timer = int(time.time()) + int(TimeOut)

while True:
		mqttc.loop()
		if( int(time.time()) >= timer ):
			try:	
				cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
				cursor = cnx.cursor()
				query = ("SELECT MAC, nummer, MQTT, id, IP, Ping FROM Core_Devices WHERE IP != 'N/A' AND IP != ''")
				printLog(debug,"Query: "+ query)
				cursor.execute(query)
				row = cursor.fetchone()
				while row is not None:
					printLog(debug,"Publish: " +  str(row[0]) + "/hostname/" + str(row[1]))
					mqttc.publish(str(row[0]) + "/hostname",str(row[1]), 0, False)
					if(int(row[2]) >= 10 ):
						MQTT = 10
					else:
						MQTT = int(row[2]) + 1
					try:	
						cnx2 = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
						cursor2 = cnx2.cursor()
						printLog(debug,"Query: UPDATE Core_Devices SET MQTT = " + str(MQTT) + " WHERE id=" + str(row[3]) )
						query2 = ("UPDATE Core_Devices SET MQTT = " + str(MQTT) + " WHERE id=" + str(row[3]) )
						cursor2.execute(query2)
						cnx2.commit()
					except Error as e:
						printLog(info,e)
					finally:	
						cursor2.close()
						cnx2.close()
						if( row[4] is not None ):
								if(int(row[5]) >= 10 ):
									PING = 10
								else:
									PING = int(row[5]) + 1

								if(ping(row[4])):
									try:
										cnx2 = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
										cursor2 = cnx2.cursor()
										printLog(debug,"Query: UPDATE Core_Devices SET Ping = 0 WHERE id=" + str(row[3]) )
										query2 = ("UPDATE Core_Devices SET Ping = 0 WHERE id=" + str(row[3]) )
										cursor2.execute(query2)
										cnx2.commit()
									except Error as e:
										printLog(info,e)
									finally:	
										cursor2.close()
										cnx2.close()
								else:
									try:	
										cnx2 = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
										cursor2 = cnx2.cursor()
										printLog(debug,"Query: UPDATE Core_Devices SET Ping = " + str(PING) + " WHERE id=" + str(row[3]) )
										query2 = ("UPDATE Core_Devices SET Ping = " + str(PING) + " WHERE id=" + str(row[3]) )
										cursor2.execute(query2)
										cnx2.commit()
									except Error as e:
										printLog(info,e)
									finally:	
										cursor2.close()
										cnx2.close()
						else:
							printLog(debug,"Query: No IP to PING")
							try:
								cnx2 = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
								cursor2 = cnx2.cursor()
								printLog(debug,"Query: UPDATE Core_Devices SET Ping = 10 WHERE id=" + str(row[3]) )
								query2 = ("UPDATE Core_Devices SET Ping = 10 WHERE id=" + str(row[3]) )
								cursor2.execute(query2)
								cnx2.commit()
							except Error as e:
								printLog(info,e)
							finally:	
								cursor2.close()
								cnx2.close()
					row = cursor.fetchone()
				timer = int(time.time()) + int(TimeOut)
			except Error as e:
				printLog(info,e)
			finally:	
				cursor.close()
				cnx.close()	