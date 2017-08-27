#!/usr/bin/env python
#Version 1.2
import sys
sys.path.append('/var/www/html/modules/libraries')
import mysql.connector
import datetime
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from inspect import currentframe
import json
from math import radians, cos, sin, asin, sqrt

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
	elif Setting == "MonitorTimeout":
		TimeOut = value
	elif Setting == "MQTT_ip_address":
		MQTT_ip_address = value
	elif Setting == "MQTT_port_python":
		MQTT_port = int(value)
	elif Setting == "MQTT_GATE_ip_address":
		MQTT_GATE_ip_address = value
	elif Setting == "MQTT_GATE_port":
		MQTT_GATE_port = int(value)
	elif Setting == "MQTT_Gate_Username":
		MQTT_Gate_Username = value
	elif Setting == "MQTT_Gate_Password":
		MQTT_Gate_Password = value
		
cursor.close()
cnx.close()	
	
debug = "DEBUG"
info = "INFO"
status = 0
CheckArr = [[]]

def printLog(level,message,Line):
	if (level.upper() == Loglevel.upper() or (level.upper() == info.upper() and Loglevel.upper() == debug.upper())):
		if(Loglevel.upper() == debug.upper()):
			strLine = " Line: "+Line
		else:
			strLine = ""
		print(level +"["+str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + "]"+strLine+" : " +str(message))

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno	
		
printLog(info,"Mobile Device Monitorring Started", str(get_linenumber()))

Timer = int(time.time())
id_arr = []
ip_arr = []
currentPing_arr = []

def Toggle(Arduino,Pin):
	mqttc.publish("arduino"+str(Arduino)+"/button"+str(Pin)+"/status", "L", 0, False)
	mqttc.publish("arduino"+str(Arduino)+"/button"+str(Pin)+"/status", "H", 0, False)
	printLog(debug,"Toggle() arduino"+Arduino+"/button"+Pin+"/Triggerd", str(get_linenumber()))

def restart():			
	subprocess.call(["sudo", "supervisorctl", "restart" ,"DeviceMonitor"])  
		
def on_connect(mqttc, obj, rc):
	printLog(debug,"rc: "+str(rc), str(get_linenumber()))

def on_message(mqttc, obj, msg):
	printLog(debug, msg.topic + "/" + msg.payload, str(get_linenumber()))
	if "/event" in msg.topic:
		try:
			owntrackid = msg.topic.split('/')
			j = json.loads(msg.payload)
			if(j['_type'] ==  "transition"):
				try:
					cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
					cursor = cnx.cursor()
					if(j['event'] == 'enter'):
						value = 'IN'
					else:
						value = 'OUT'
					query = ("UPDATE OwnTracks_User_Status SET Status='"+value+"' WHERE waypoint_ID = (SELECT id FROM OwnTracks_Waypoint WHERE Naam = '"+j['desc']+"') AND Monitor_Devices_ID = (SELECT id FROM Monitor_Devices WHERE ownTracksID = '"+owntrackid[2]+"')")
					printLog(debug,"UPDATE OwnTracks_User_Status SET Status='"+value+"' WHERE waypoint_ID = (SELECT id FROM OwnTracks_Waypoint WHERE Naam = '"+j['desc']+"') AND Monitor_Devices_ID = (SELECT id FROM Monitor_Devices WHERE ownTracksID = '"+owntrackid[2]+"')", str(get_linenumber()))	
					cursor.execute(query)
					cnx.commit()
				except Exception as e:
					printLog(info,e, str(get_linenumber())) 
				finally:	
					cursor.close()
					cnx.close()
				try:
					cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
					cursor = cnx.cursor()
					query = ("SELECT arduino, pin FROM Owntracks_action INNER JOIN Core_vButtonDB ON  Owntracks_action.Core_vButtonDB = Core_vButtonDB.id WHERE ownTracks_event = '"+j['event']+"' AND Monitor_Devices_id = ( SELECT id from Monitor_Devices WHERE ownTracksID = '"+owntrackid[2]+"') and OwnTracks_Waypoint = (SELECT id FROM OwnTracks_Waypoint WHERE Naam = '"+j['desc']+"')")
					printLog(debug,"Query: "+query, str(get_linenumber()))
					cursor.execute(query)
					for (arduino, pin) in cursor:
						Toggle(str(arduino),str(pin))
				except Exception as e:
					printLog(info,e, str(get_linenumber())) 
				finally:	
					cursor.close()
					cnx.close()
						
				
				
		except Exception as e:
					printLog(info,e, str(get_linenumber()))
	
	
	if "gateway/getList" in msg.topic:
		subscribe_clients()
		

		
def on_publish(mqttc, obj, mid):
	printLog(debug,"mid: "+str(mid), str(get_linenumber()))

def on_subscribe(mqttc, obj, mid, granted_qos):
    printLog(debug,"Subscribed: "+str(mid)+" "+str(granted_qos), str(get_linenumber()))

def on_log(mqttc, obj, level, string):
    printLog(debug,string, str(get_linenumber()))

def on_disconnect(client, userdata, rc):
	logger.printLog(info, "on_disconnect!", str(logger.get_linenumber()))
	exit()	
	
def subscribe_clients():
	try:
		cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
		cursor = cnx.cursor()
		cursor.execute("SELECT ownTracksID FROM Monitor_Devices WHERE ownTracksID != ''")
		maxid = 0
		for (ownTracksID) in cursor:
			printLog(debug,"Subscribe: owntracks/+/" + str(ownTracksID[0]), str(get_linenumber()))
			mqttc.subscribe("owntracks/+/" + str(ownTracksID[0]), 0)
			printLog(debug,"Subscribe: owntracks/+/" + str(ownTracksID[0]) + "/event", str(get_linenumber()))
			mqttc.subscribe("owntracks/+/" + str(ownTracksID[0]) + "/event", 0)
			# printLog(debug,"Publish: gateway/subscribe/owntrack/" + str(ownTracksID[0]), str(get_linenumber()))
			publish.single( "gateway/subscribe/owntrack",str(ownTracksID[0]) + "/event", hostname=MQTT_GATE_ip_address,  port=MQTT_GATE_port,retain=False, auth = {'username':MQTT_Gate_Username, 'password':MQTT_Gate_Password})
	except Exception as e:
			printLog(info,e,str(get_linenumber())) 
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
		print ("Sleep")
		time.sleep(5)

printLog(info,"Connected",str(get_linenumber()))

printLog(debug,"Subscribe: gateway/getList", str(get_linenumber()))
mqttc.subscribe("gateway/getList", 0)	

subscribe_clients()
		
while True:
	mqttc.loop()
