#!/usr/bin/env python
#Version 5.5
"""
Created on Sun Jan 16 2017

@author: Laurent
"""
import sys
sys.path.append('/var/www/html/modules/libraries')
from astral import *
from time import gmtime,strftime
import datetime
import paho.mqtt.client as mqtt

import os
import time
import string
import smtplib
import mysql.connector
import subprocess
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
	print("query: "+query)
	cursor.execute(query)	
	for (Setting, value) in cursor:
		if Setting == "MQTT_ip_address":
			MQTT_ip_address = value
		elif Setting == "MQTT_port_python":
			MQTT_port = value
		elif Setting == "loglevel":
			Loglevel = value
		elif Setting == "Location":
			city_name = value
except Exception as e:
	printLog(info,e, str(get_linenumber())) 
finally:		
	cursor.close()	
	cnx.close()
	
debug = "DEBUG"
info = "INFO"
CoreService = "Core"

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


		
try:
	cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	try:
		query = "SELECT MAX(DISTINCT arduino) FROM Core_vButtonDB"
		printLog(info,"Query "+query, str(get_linenumber())) 
		cursor.execute(query)
		result=cursor.fetchone()
		number_of_arduino = result[0] + 1
	except Exception as e:
		number_of_arduino = int(0)
		printLog(info,e, str(get_linenumber())) 
	
	try:
		cursor.execute("SELECT MAX(id) FROM html_Radio")
		result=cursor.fetchone()
		number_of_kodi = result[0]
	except Exception as e:
		number_of_kodi = int(0)
		printLog(info,e, str(get_linenumber())) 
finally:	
	cursor.close()
	cnx.close()

#ThreeDArray=np.zeros((4,3,16), dtype=np.object)
ThreeDArray= [ [ [ "0" for z in range(16) ] for e in range(number_of_arduino) ] for r in range(4) ]

Custom_TIMER_LAURENT = 0

# 3d Array
# row 0 Buttons
# row 1 DelayButtons
# row 2 FirstActions Button
# row 3 SecondActions Button

RelayStatus = []
DimmerInAction = []
RelayStatusCheck2 = []
ButtonPushed = []
ButtonMessage = []
VButtonArray = []
ButtonTimerArray = []
ButtonOffsetArray = []
DelayTimer = []
RelayTimer = []
RelayOnTimer = []
RelayOffTimer = []
DimmerOnTimer = []
DimmerOffTimer = []
DimmerOnTimerValue = []
DimmerOffTimerValue = []
WaitTimer = []
WaitTime = []
ButtonDimmerDirection = []
RelayDimmerDirection = []
ButtonDimmerSpeed = []
RelayDimmerValue = []
RelayDimmerStatus = []
ButtonDimmerAction = []
ButtonDimmerTimer = []
ButtonDimmerTimer2 = []
ButtonDimmerOffset = []
RealTimeDimmerValue = []
KodiStatus = [number_of_kodi]


for i in xrange(number_of_arduino):
	RelayStatus.append([])
	DimmerInAction.append([])
	RelayStatusCheck2.append([])
	ButtonPushed.append([])
	ButtonMessage.append([])
	VButtonArray.append([])
	ButtonTimerArray.append([])
	ButtonOffsetArray.append([])
	DelayTimer.append([])
	RelayTimer.append([])
	RelayOnTimer.append([])
	RelayOffTimer.append([])
	DimmerOnTimer.append([])
        DimmerOffTimer.append([])
	DimmerOnTimerValue.append([])
        DimmerOffTimerValue.append([])
	WaitTimer.append([])
	WaitTime.append([])
	ButtonDimmerDirection.append([])
	RelayDimmerDirection.append([])
	ButtonDimmerSpeed.append([])
	RelayDimmerValue.append([])
	RelayDimmerStatus.append([])
	ButtonDimmerAction.append([])
	ButtonDimmerTimer.append([])
	ButtonDimmerTimer2.append([])
	ButtonDimmerOffset.append([])
	RealTimeDimmerValue.append([])
	for j in xrange(16):
		RelayStatus[i].append(0)
		DimmerInAction[i].append(0)
		RelayStatusCheck2[i].append(0)
		ButtonPushed[i].append(0)
		ButtonMessage[i].append(0)
		VButtonArray[i].append(0)
		ButtonTimerArray[i].append(0)
		ButtonOffsetArray[i].append(0)
		DelayTimer[i].append(0)
		RelayTimer[i].append(0)
		RelayOnTimer[i].append(-1)
		RelayOffTimer[i].append(-1)
		DimmerOnTimer[i].append(-1)
                DimmerOffTimer[i].append(-1)
		DimmerOnTimerValue[i].append(-1)
		DimmerOffTimerValue[i].append(-1)
		WaitTimer[i].append(0)
		WaitTime[i].append(0)
		RelayDimmerDirection[i].append(0)
		ButtonDimmerSpeed[i].append(0)
		RelayDimmerValue[i].append(0)
		RelayDimmerStatus[i].append(0)
		ButtonDimmerAction[i].append(0)
		ButtonDimmerTimer[i].append(0)
		ButtonDimmerTimer2[i].append(0)
		ButtonDimmerOffset[i].append(0)
		RealTimeDimmerValue[i].append(0)

# ButtonDimmerDirection = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# ButtonDimmerSpeed = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# RelayDimmerValue = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# RelayDimmerValueCheck = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# RelayDimmerStatus = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# ButtonDimmerAction = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# ButtonDimmerTimer = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# ButtonDimmerTimer2 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# ButtonDimmerOffset = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
# RelayDimmerValueSent = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]




# Dimmer topics
#   Arduino0/dimmer0/value
#   Arduino0/dimmer0/direction
#specify Arduino button actions
#R = relay
#M = mail
#On = On
#Off = Off
#D = Delay
#SD = Sun Down
#CO = Condition Or
#CA = Condition And
#E = End
#TE = The End -> niet nodig
#T = Toggle
#W = Wait till button released (for motion detection)
#FBLWR -> FBL with feedback relais
#FBL = Place before R -> Controls a FeedBackLight for the given Button ex. "1|W|1800|FBL|0|1|R|2|15|Off|300|E"
#RFBL = Place before R -> Controls a FeedBackLight for the given Button ex. "1|W|1800|FBL|0|1|R|2|15|Off|300|E" returns the opposite/Reverse as FBL
#BTF = ButtonTimer perform action after a certain button hold time ex. "3|2|R|0|1|T|E|BTF|R|0;0|1;2|Off|0|E" BTF -> ButtonTimerFirst action / ButtonTimerSecond action after a hold time of 2 sec
#BD = ButtonDimmer "3|2|BD|-1|10000|0|1|E|R|0;0|1;2|Off|0|E|BTF|R|0;0|1;2|BD|75|10000|0|3|E" -> -1 use previous vallue, value between 0 and 100 filed in below 127 go up oterhwise go down, next value speed in milliseconds to have full value
# first place of action string MUST be a number :
#            0 -> perform action after release
#            1 -> perform action immediately
#            2 -> send a command for the dimmer
#            3 -> wait a moment for a second action

#Mail setup
def MailSend(ReceiveList):
 ReceiveList2 = ReceiveList.split(";")
 for v in range (len(ReceiveList2)):
  sender = "laurent.michel1@telenet.be"
  receivers = ReceiveList2[v]
  message = """From: laurent.michel1@telenet.be
To: """ + ReceiveList2[v] + """
Subject: Alarm melding

Er is beweging gedetecteerd op volgend circuit
""" + sender + """ Alarm """

  smtpObj = smtplib.SMTP('uit.telenet.be')
  smtpObj.sendmail(sender, receivers, message)         

###############
def FirstBA(ArduinoN,ButtonN,NumberN,ArrayN):
 ButtonList = ThreeDArray[ArrayN][ArduinoN][ButtonN].split("|")
 ButtonBA = int(ButtonList[NumberN])
 return ButtonBA

def WaitBA(ArduinoN,ButtonN,ArrayN):
 ButtonList = ThreeDArray[ArrayN][ArduinoN][ButtonN].split("|")
 ButtonBA = str(ButtonList[1])
 if (ButtonBA == "W"):
  ButtonWA = int(ButtonList[2])
 else:
  ButtonWA = 0
 return ButtonWA

#def ButtonDelay():

# def updateStatus(Arduino,Relais,status):
	# cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
	# cursor = cnx.cursor()
	# query = ("UPDATE Core_Arduino_Outputs SET status = '"+status+"' WHERE arduino = " + Arduino + " and pin = " + Relais)
	# printLog(debug,"UPDATE Core_Arduino_Outputs SET status = '"+status+"' WHERE arduino = " + Arduino + " and pin = " + Relais, str(get_linenumber()))
	# cursor.execute(query)
	# cnx.commit()
	# cursor.close()
	# cnx.close()

def restart():			
	printLog(info,CoreService +" service has been restarted by the script" , str(get_linenumber()))
	subprocess.call(["sudo", "supervisorctl", "restart" ,CoreService]) 

def on_connect(mqttc, obj, rc):
 printLog(info,"rc: "+str(rc) , str(get_linenumber()))

def on_message(mqttc, obj, msg):
 global R3Status
 global button3on
 global button3off
 global R4Status
 global button4on
 global button4off
 printLog(info, "on_message: " + msg.topic + "/" + msg.payload  , str(get_linenumber()))
 if msg.topic == CoreService + "/service/restart":
	restart();
# relays 22 to 37 are defined
# volgende moet een twee dimensionale array worden vermits ALLE arduinos plus ALLE relais moeten doorlopen worden
 for i in range (len(KodiStatus)):
   if (msg.topic == "kodi" + str(i) + "/status/playbackstate" and int(msg.payload) > -1):
     KodiStatus[i] = int(msg.payload)
		
 for i in range (len(RelayDimmerStatus)):
  for z in range (len(RelayDimmerStatus[i])):
   #mqttc.publish("arduino" + str(i) + "/dimmer" + str(z) + "/status", 0, 0, True)
   if (msg.topic == "arduino" + str(i) + "/dimmer"+ str(z) +"/status" and int(msg.payload) > -1):
    RealTimeDimmerValue[i][z] = int(msg.payload)
    RelayDimmerStatus[i][z] = 1
    RelayDimmerValue[i][z] = int(msg.payload)
   if (msg.topic == "arduino" + str(i) + "/dimmer"+ str(z) +"/status" and int(msg.payload) == -1):
    RelayDimmerStatus[i][z] = 0
 for i in range (len(RelayStatus)):
  for z in range (len(RelayStatus[i])):
   if (msg.topic == "arduino" + str(i) + "/relais"+ str(z) +"/status" and str(msg.payload) == "L"):
    RelayStatus[i][z] = 0
    #updateStatus(str(i),str(z),'OFF')
   if (msg.topic == "arduino" + str(i) + "/relais"+ str(z) +"/status" and str(msg.payload) == "H"):
    RelayStatus[i][z] = 1
    #updateStatus(str(i),str(z),'ON')
 for i in range (len(ButtonPushed)):
  #printLog(info,msg.topic + " = ? -> arduino" + str(i) + "/radio/volume and with payload" + str(msg.payload) , str(get_linenumber()))
  if (msg.topic == "arduino" + str(i) + "/radio/volume" and int(msg.payload) > -1):
      printLog(info,"arduino" + str(i) + "/radio/volume " + str(msg.payload) , str(get_linenumber()))
      RadioList = ThreeDArray[0][i][7].split("|")
      for g in range (len(RadioList)):
       if (RadioList[g] == "K"):
        RadioList2 = RadioList[g+1]
	for e in range (len(RadioList2)):
         mqttc.publish("kodi" + RadioList2[e] + "/command/volume", str(msg.payload), 0, True)
	 printLog(info,"publish kodi" + RadioList2[e] + "/command/volume/" + str(msg.payload) , str(get_linenumber()))
  if (msg.topic == "arduino" + str(i) + "/radio/channel" and int(msg.payload) > -1):
      RadioList = ThreeDArray[0][i][7].split("|")
      for g in range (len(RadioList)):
       if (RadioList[g] == "K"):
        RadioList2 = RadioList[g+1]
	for e in range (len(RadioList2)):
         mqttc.publish("kodi" + RadioList2[e] + "/command/play", GetChannel(msg.payload), 0, True)
	 printLog(info,"publish kodi" + RadioList2[e] + "/command/play/" + GetChannel(msg.payload) , str(get_linenumber()))
  for z in range (len(ButtonPushed[i])):
   if (ThreeDArray[0][i][z] != ""):
    if (msg.topic == "arduino" + str(i) + "/button"+ str(z) +"/status" and str(msg.payload) == "L" and FirstBA(i,z,0,0) == 0 and ButtonPushed[i][z] == 0):
     ButtonPushed[i][z] = 1
     printLog(info,"arduino" + str(i) + "/button"+ str(z) +"/status" +  str(msg.payload) , str(get_linenumber()))
    if (msg.topic == "arduino" + str(i) + "/button"+ str(z) +"/status" and str(msg.payload) == "L" and FirstBA(i,z,0,0) == 1 and ButtonPushed[i][z] == 0 and WaitBA(i,z,0) == 0):
      ButtonPushed[i][z] = 1
      ButtonAction2(i,z,0)
      printLog(info,"arduino" + str(i) + "/button"+ str(z) +"/status" +  str(msg.payload) , str(get_linenumber()))
#   if (msg.topic == "arduino" + str(i) + "/button"+ str(z) +"/status" and str(msg.payload) == "L" and FirstBA(i,z,0,0) == 2 and ButtonPushed[i][z] == 0):
#     ButtonPushed[i][z] = 1
#     ButtonDimmer(i,z,"L")
#     printLog(info,"arduino" + str(i) + "/button"+ str(z) +"/status" +  str(msg.payload) , str(get_linenumber()))
#   if (msg.topic == "arduino" + str(i) + "/button"+ str(z) +"/status" and str(msg.payload) == "H" and FirstBA(i,z,0,0) == 2 and ButtonPushed[i][z] == 1):
#     ButtonPushed[i][z] = 0
#     ButtonDimmer(i,z,"H")
#     printLog(info,"arduino" + str(i) + "/button"+ str(z) +"/status" +  str(msg.payload) , str(get_linenumber()))
    if (msg.topic == "arduino" + str(i) + "/button"+ str(z) +"/status" and str(msg.payload) == "L" and FirstBA(i,z,0,0) == 3 and ButtonPushed[i][z] == 0 and ButtonTimerArray[i][z] == 0):
     ButtonPushed[i][z] = 1
     ButtonTimerArray[i][z] = 1
     ButtonOffsetArray[i][z] = int(time.time()) + int(FirstBA(i,z,1,0))
     printLog(info,"arduino" + str(i) + "/button"+ str(z) +"/status" +  str(msg.payload) , str(get_linenumber()))
    if (msg.topic == "arduino" + str(i) + "/button"+ str(z) +"/status" and str(msg.payload) == "H" and FirstBA(i,z,0,0) == 3 and ButtonPushed[i][z] == 1):
     ButtonPushed[i][z] = 0
     printLog(info,"ButtonTimerArray[i][z]: "+str(ButtonTimerArray[i][z]), str(get_linenumber()))
     if (ButtonTimerArray[i][z] == 2):
      ButtonTimerArray[i][z] = 0
      ButtonDimmerAction[i][z] = 0
      ButtonFirstAction = ThreeDArray[0][i][z].split("BTF")
      SecondAction = ButtonFirstAction[0]
      SecondActionArray = SecondAction.split("|")
      for g in range (len(SecondActionArray)):
       if (SecondActionArray[g] == "BD"):
        DimmerArduino = SecondActionArray[g + 3]
        DimmerRelay = SecondActionArray[g + 4]
	DimmerArduinoArray = DimmerArduino.split(";")
	DimmerRelayArray = DimmerRelay.split(";")
     if (ButtonTimerArray[i][z] == 1):
       ButtonTimerArray[i][z] = 0
       ButtonFirstAction = ThreeDArray[0][i][z].split("BTF")
       ThreeDArray[2][i][z] = ButtonFirstAction[1]
       ButtonAction2(i,z,2)
       printLog(info,"arduino" + str(i) + "/button"+ str(z) +"/status" +  str(msg.payload) , str(get_linenumber()))
    if (msg.topic == "arduino" + str(i) + "/button"+ str(z) +"/status" and str(msg.payload) == "L" and FirstBA(i,z,0,0) == 1 and ButtonPushed[i][z] == 0 and WaitBA(i,z,0) > 0):
     printLog(info,"arduino" + str(i) + "/button"+ str(z) +"/status" +  str(msg.payload) , str(get_linenumber()))
     printLog(debug,WaitBA(i,z,0) , str(get_linenumber()))
     ButtonMessage[i][z] = "L"
     ButtonAction2(i,z,0)
     ButtonPushed[i][z] = 1
     WaitTimer[i][z] = 5
    if (ButtonPushed[i][z] == 1 and msg.topic == "arduino" + str(i) + "/button"+ str(z) +"/status" and FirstBA(i,z,0,0) == 0 and str(msg.payload) == "H"):
     ButtonAction2(i,z,0)
     ButtonPushed[i][z] = 0
     printLog(info,"arduino" + str(i) + "/button"+ str(z) +"/status" +  str(msg.payload) , str(get_linenumber()))
    if (ButtonPushed[i][z] == 1 and msg.topic == "arduino" + str(i) + "/button"+ str(z) +"/status" and FirstBA(i,z,0,0) == 1 and str(msg.payload) == "H"):
     ButtonPushed[i][z] = 0
     ButtonMessage[i][z] = "H"
     printLog(info,"arduino" + str(i) + "/button"+ str(z) +"/status" +  str(msg.payload) , str(get_linenumber()))

 #CheckVButton(0)

def on_publish(mqttc, obj, mid):
    printLog(info,"mid: "+str(mid) , str(get_linenumber()))

def on_subscribe(mqttc, obj, mid, granted_qos):
    printLog(info,"Subscribed: "+str(mid)+" "+str(granted_qos) , str(get_linenumber()))

def on_disconnect(client, userdata, rc):
	printLog(info, "on_disconnect!", str(get_linenumber()))
	exit()

def on_log(mqttc, obj, level, string):
    printLog(info,string , str(get_linenumber()))
	
def GetChannel(ChannelNumber):
	url = ""
	#Get url from database
	try:
		cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
		cursor = cnx.cursor()
		query = ("SELECT url FROM html_Radio_zenders WHERE id = " + ChannelNumber )
		printLog(debug,"Query: "+query,str(get_linenumber()))
		cursor.execute(query)
		row = cursor.fetchone()
		while row is not None:
			url = str(row[0])
			printLog(debug,"URL: "+url,str(get_linenumber()))
			if "www.youtube.com" in url:
				tmpArr = []
				tmpArr = url.split('/')
				youtubeId = tmpArr[len(tmpArr) - 1];
				youtubeId = youtubeId.replace("watch?v=","");
				url = '{ "item": { "file":"plugin://plugin.video.youtube/?action=play_video&videoid='+youtubeId+'"}}';
			row = cursor.fetchone()
	except Exception as e:
		printLog(info,e) 
	finally:	
		cursor.close()
		cnx.close()
		return str(url)
 
# def GetChannel(ChannelNumber):
  # url = "http://mp3.streampower.be/ra2vlb-mid"
  # printLog(debug,"Query: SELECT url FROM html_Radio_zenders WHERE id = " + ChannelNumber,str(get_linenumber()))
  # return url

def SunDown(before, after):
 a = Astral()
 timeToday = int(time.strftime("%Y%m%d%H%M%S",gmtime()))
 city = a[city_name]
 date = datetime.date.today()
 sun = city.sun(date, local=True)
 # sunrise = a.sunrise_utc(date,50.8000,4.9333)
 # sunset = a.sunset_utc(date,50.8000,4.9333)
 before = before.replace('+','')
 after = after.replace('+','')
 
 sunrise = sun['sunrise'] + datetime.timedelta(minutes=int(before)) 
 sunset = sun['sunset'] + datetime.timedelta(minutes=int(after))


 sunsetint = int('{0}{1}{2}{3}{5}{6}{8}{9}{11}{12}{14}{15}{17}{18}'.format(*str(sunset)))
 sunriseint = int('{0}{1}{2}{3}{5}{6}{8}{9}{11}{12}{14}{15}{17}{18}'.format(*str(sunrise)))
 sunsetHour = int('{11}{12}'.format(*str(sunset)))
 sunriseHour = int('{11}{12}'.format(*str(sunrise)))
 sunsetHour = sunsetHour - 1
 sunriseHour = sunriseHour + 1
 sunsetint = int(str('{0}{1}{2}{3}{5}{6}{8}{9}'.format(*str(sunset))) + str(sunsetHour) + str('{14}{15}{17}{18}'.format(*str(sunset))))
 sunriseint = int(str('{0}{1}{2}{3}{5}{6}{8}{9}'.format(*str(sunrise))) + "0" + str(sunriseHour) + str('{14}{15}{17}{18}'.format(*str(sunrise))))

 if(timeToday > sunriseint and timeToday < sunsetint):
  printLog(info,"zon is op" , str(get_linenumber()))
  return "false"
 else:
  printLog(info,"zon is onder" , str(get_linenumber()))
  return "true"

def checkOwntracks(owntrackID,conditie):		
	try:
		cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
		cursor = cnx.cursor()
		query = "SELECT count(*) FROM OwnTracks_User_Status WHERE  waypoint_ID="+owntrackID+" ANd Status != 'OUT'"
		printLog(debug,"Query: "+query,str(get_linenumber()))
		cursor.execute(query)
	
		result=cursor.fetchone()
		if((conditie == 'WPO' and result[0] == 0) or (conditie == 'WPI' and result[0] > 0)):
			return True
		else:
			return False
	except Exception as e:
		printLog(info,e, str(get_linenumber()))
		return False
	finally:	
		cursor.close()
		cnx.close()  
  
def RelayChecker(ArduinoNumberC,RelayNumberC,Condition):
 printLog(debug,"go check conditions ", str(get_linenumber()))
 ArduinoList = ArduinoNumberC.split(";")
 RelayList = RelayNumberC.split(";")
 CorTrue = 0
 CandFalse = 0
 Reverse = 2
 for a in range (len(ArduinoList)):
  if ("!" in RelayList[a]):
    RelayCheckedA = RelayList[a].split("!")
    RelayChecked = RelayCheckedA[1]
    Reverse = 1
    printLog(debug,"! in relay so reverse for Arduino " + ArduinoList[a] + " and relay " + RelayChecked, str(get_linenumber()))
  else:
    RelayChecked = RelayList[a]
    Reverse = 0
    printLog(debug,"NO ! in relay so NO reverse for Arduino " + ArduinoList[a] + " and relay " + RelayChecked, str(get_linenumber()))
  if ((RelayStatus[int(ArduinoList[a])][int(RelayChecked)] == 1 and Reverse == 0) or (RelayStatus[int(ArduinoList[a])][int(RelayChecked)] == 0 and Reverse == 1) ):
   if (Condition == 0):
    CorTrue = 1
  if ((RelayStatus[int(ArduinoList[a])][int(RelayChecked)] == 0 and Reverse == 0) or (RelayStatus[int(ArduinoList[a])][int(RelayChecked)] == 1 and Reverse == 1)):
   if (Condition == 1):
    CandFalse = 1
 if (Condition == 0):
  if (CorTrue == 1):
   return "true"
  else:
   return "false"
 if (Condition == 1):
  if (CandFalse == 1):
   return "false"
  else:
   return "true"


def ExtendOffTimer(ArduinoNumber,InputNumber,ArrayN):
 ButtonList = ThreeDArray[ArrayN][ArduinoNumber][InputNumber].split("|")
 RelayOFF = 0
 for i in range (len(ButtonList)):
  if (ButtonList[i] == "R"):
   ArduinoNumber = ButtonList[i + 1]
   RelayNumber = ButtonList[i + 2]
  if (ButtonList[i] == "Off"):
   RelayOFF = int(ButtonList[i + 1])
 ArduinoList = ArduinoNumber.split(";")
 RelayList = RelayNumber.split(";")
 for c in range (len(ArduinoList)):
  RelayOffTimer[int(ArduinoList[c])][int(RelayList[c])] = int(time.time()) + RelayOFF

def ButtonDimmerOff(Arduino_number,button_pushed_int,DimmerValue,DimmerArduino,DimmerRelay,DimmerSpeed):
 ArduinoDimmerList = DimmerArduino.split(";")
 RelayDimmerList = DimmerRelay.split(";")        
 for f in range (0,1):
  if (RelayStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 1):
   if (RelayDimmerStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 0):
    ButtonDimmerAction[Arduino_number][button_pushed_int] =  "OFF|" + "100" + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay
   if (RelayDimmerStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 1):
    ButtonDimmerAction[Arduino_number][button_pushed_int] =  "OFF|" + str(RealTimeDimmerValue[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])]) + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay	  
  else:
   printLog(debug,"nothing to do" , str(get_linenumber()))

def ButtonDimmerOn(Arduino_number,button_pushed_int,DimmerValue,DimmerArduino,DimmerRelay,DimmerSpeed):
 ArduinoDimmerList = DimmerArduino.split(";")
 RelayDimmerList = DimmerRelay.split(";")      
 for f in range (0,1):
  if (RelayStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 0):
   if (int(DimmerValue) == -1): 
    ButtonDimmerAction[Arduino_number][button_pushed_int] =  "ON|" + str(RealTimeDimmerValue[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])]) + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay
    for a in range (len(ArduinoDimmerList)):
     RelayDimmerValue[int(ArduinoDimmerList[a])][int(RelayDimmerList[a])] = 0
   if (int(DimmerValue) > -1):
    ButtonDimmerAction[Arduino_number][button_pushed_int] =  "ON|" + DimmerValue + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay
    for a in range (len(ArduinoDimmerList)):
     RelayDimmerValue[int(ArduinoDimmerList[a])][int(RelayDimmerList[a])] = 0
  else:
   printLog(debug,"nothing to do" , str(get_linenumber()))

def CheckVButton(ArrayN):
 VButton = 0
 FBLight = 0
 RFBLight = 0
 CFBLight = 0
 RCFBLight = 0
 HasPhysicFBL = 0
 ToggleCheckA = ""
 ToggleCheckR = ""
 OnCheckA = ""
 OnCheckR = ""
 OffCheckA = ""
 OffCheckR = ""
 ToggleCheckArrayA = ""
 ToggleCheckArrayR = ""
 OnCheckArrayA = ""
 OnCheckArrayR = ""
 OffCheckArrayA = ""
 OffCheckArrayR = ""
 ToggleL = 0
 OnL = 0
 OffL = 0
 ButtonDimmer = 0
 RelayON = 0
 RelayOFF = 0
 IsToggled = 0
 ButtonRelay = 0
 ToggleVButton = 0
 OnVButton = 0
 ROffVButton = 0
 OffVButton = 0
 for i in range (len(ThreeDArray[ArrayN])):
  for z in range (len(ThreeDArray[ArrayN][i])):
  # 3|2|BD|-1|5000|0|1|E|R|0|2|Off|0|E|BTF|BD|-1|1000|0|1|R|0|2|T|E
  # 3|2|BD|-1|5000|0|1|E|R|0|2|Off|0|E|BTF|BD|-1|1000|0|1|R|0|2|T|E
    #ButtonListFA = 
    ButtonList = ThreeDArray[ArrayN][i][z].split("|")

    for j in range (len(ButtonList)):

      if (ButtonList[j] == "FBL"):
        ArduinoFBL = ButtonList[j+1].split(";")
	RelayFBL = ButtonList[j+2].split(";")
	if (ArduinoFBL[0].isdigit()):
	 HasPhysicFBL = 1
	FBLight = 1
      if (ButtonList[j] == "RFBL"):
        ArduinoFBL = ButtonList[j+1].split(";")
	RelayFBL = ButtonList[j+2].split(";")
	if (ArduinoFBL[0].isdigit()):
	 HasPhysicFBL = 1
	RFBLight = 1
      if (ButtonList[j] == "CFBL"):
        ArduinoFBL = ButtonList[j+1].split(";")
	RelayFBL = ButtonList[j+2].split(";")
	if (ArduinoFBL[0].isdigit()):
	 HasPhysicFBL = 1
	CFBLight = 1
      if (ButtonList[j] == "RCFBL"):
        ArduinoFBL = ButtonList[j+1].split(";")
	RelayFBL = ButtonList[j+2].split(";")
	if (ArduinoFBL[0].isdigit()):
	 HasPhysicFBL = 1
	RCFBLight = 1
      if (FBLight == 1 or RFBLight == 1 or CFBLight == 1 or RCFBLight == 1):
       if (ButtonList[j] == "BD"):
        ButtonDimmer = 1
        DimmerArduino = ButtonList[j + 3]
        DimmerRelay = ButtonList[j + 4]
       if (ButtonList[j] == "R"):
        ButtonRelay = 1
        ArduinoNumber = ButtonList[j + 1]
        RelayNumber = ButtonList[j + 2]
       if (ButtonList[j] == "On"):
        RelayON = 1
       if (ButtonList[j] == "T"):
        printLog(info,"toggled ? "+str(ButtonList[i]) , str(get_linenumber()))
        IsToggled = 1
       if (ButtonList[j] == "Off"):
        RelayOFF = 1
       if (ButtonList[j] == "E"):
        if (IsToggled == 1):
	 if (ButtonDimmer == 1):	 
          ToggleCheckR += DimmerRelay if ToggleCheckR == "" else ";" + DimmerRelay
	  ToggleCheckA += DimmerArduino if ToggleCheckA == "" else ";" + DimmerArduino
	 if (ButtonRelay == 1):	 
          ToggleCheckR += RelayNumber if ToggleCheckR == "" else ";" + RelayNumber
	  ToggleCheckA += ArduinoNumber if ToggleCheckA == "" else ";" + ArduinoNumber
        if (RelayON == 1):
	 if (ButtonDimmer == 1):	 
          OnCheckR += DimmerRelay if OnCheckR == "" else ";" + DimmerRelay
	  OnCheckA += DimmerArduino if OnCheckA == "" else ";" + DimmerArduino
	 if (ButtonRelay == 1):	 
          OnCheckR += RelayNumber if OnCheckR == "" else ";" + RelayNumber
	  OnCheckA += ArduinoNumber if OnCheckA == "" else ";" + ArduinoNumber
        if (RelayOFF == 1):
	 if (ButtonDimmer == 1):	 
          OffCheckR += DimmerRelay if OffCheckR == "" else ";" + DimmerRelay
	  OffCheckA += DimmerArduino if OffCheckA == "" else ";" + DimmerArduino
	 if (ButtonRelay == 1):	 
          OffCheckR += RelayNumber if OffCheckR == "" else ";" + RelayNumber
	  OffCheckA += ArduinoNumber if OffCheckA == "" else ";" + ArduinoNumber
	ButtonDimmer = 0
	RelayON = 0
	RelayOFF = 0
	IsToggled = 0
	ButtonRelay = 0
	
    ToggleCheckArrayA = ToggleCheckA.split(";")
    ToggleCheckArrayR = ToggleCheckR.split(";")
    OnCheckArrayA = OnCheckA.split(";")
    OnCheckArrayR = OnCheckR.split(";")
    OffCheckArrayA = OffCheckA.split(";")
    OffCheckArrayR = OffCheckR.split(";")
    if ToggleCheckR:
	ToggleL = len(ToggleCheckArrayA)
	printLog(info,"CheckT " + str(VButton) , str(get_linenumber()))
	for d in range (len(ToggleCheckArrayA)):
		printLog(debug,"status T van "+ str(ToggleCheckArrayA[d]) + " " + str(ToggleCheckArrayR[d]) + " " + str((RelayStatus[int(ToggleCheckArrayA[d])][int(ToggleCheckArrayR[d])])) , str(get_linenumber()))
		if (RelayStatus[int(ToggleCheckArrayA[d])][int(ToggleCheckArrayR[d])] == 1):
			ToggleVButton = ToggleVButton + 1
			printLog(debug,"ToggleVButton_teller1 " + str(ToggleVButton) , str(get_linenumber()))
			
    if OnCheckR:
	OnL = len(OnCheckArrayA)
	printLog(debug,"CheckOn " + str(VButton) , str(get_linenumber()))
	for d in range (len(OnCheckArrayA)):
		printLog(debug,"status On " + str((RelayStatus[int(OnCheckArrayA[d])][int(OnCheckArrayR[d])])), str(get_linenumber()))
		if (RelayStatus[int(OnCheckArrayA[d])][int(OnCheckArrayR[d])] == 1):
			OnVButton = OnVButton + 1
			printLog(debug,"OnVButton_teller2 " + str(OnVButton) , str(get_linenumber()))
			
    if OffCheckR:
	OffL = len(OffCheckArrayA)
	printLog(info,"CheckOff " + str(VButton) , str(get_linenumber()))
	for d in range (len(OffCheckArrayA)):
		if (RelayStatus[int(OffCheckArrayA[d])][int(OffCheckArrayR[d])] == 0):
			OffVButton = OffVButton + 1
			printLog(debug,"OffVButton_teller3 " + str(OffVButton) , str(get_linenumber()))
		else:
		        ROffVButton = ROffVButton + 1
			printLog(debug,"ROffVButton_teller4 " + str(ROffVButton) , str(get_linenumber()))
    #onderstaande print NIET activeren enkel voor debug		
    #printLog(debug,"lengte T " + str(ToggleL) + " lengte On " + str(OnL) + " Lengte Off " + str(OffL) + " samen " + str(ToggleL+OnL+OffL) , str(get_linenumber()))
    if ((ToggleVButton+OnVButton+OffVButton) == (ToggleL+OnL+OffL) and CFBLight == 1 and VButtonArray[i][z] == 0):
	printLog(debug,"hoeveel lichten maar blijkbaar gelijk " + str(VButton), str(get_linenumber()))
	printLog(info,"Change of Vbutton status!" , str(get_linenumber()))
	VButtonArray[i][z] = 1
	mqttc.publish("arduino" + str(i) + "/vbutton" + str(z) + "/status", "H", 0, True)
	if (HasPhysicFBL == 1):
	 for q in range (len(ArduinoFBL)):
	  mqttc.publish("arduino" + ArduinoFBL[q] + "/relais" + RelayFBL[q] + "/action", "H", 0, False)
    if ((ToggleVButton+OnVButton+OffVButton) != (ToggleL+OnL+OffL) and CFBLight == 1 and VButtonArray[i][z] == 1):
	printLog(info,"Change of Vbutton status!" , str(get_linenumber()))
	VButtonArray[i][z] = 0
	mqttc.publish("arduino" + str(i) + "/vbutton" + str(z) + "/status", "L", 0, True)
	if (HasPhysicFBL == 1):
	 for q in range (len(ArduinoFBL)):
	  mqttc.publish("arduino" + ArduinoFBL[q] + "/relais" + RelayFBL[q] + "/action", "L", 0, False)
    if ((ToggleVButton+OnVButton+OffVButton) > 0 and RCFBLight == 1 and VButtonArray[i][z] == 0):
	VButtonArray[i][z] = 1
	mqttc.publish("arduino" + str(i) + "/vbutton" + str(z) + "/status", "H", 0, True)
	if (HasPhysicFBL == 1):
	 for q in range (len(ArduinoFBL)):
	  mqttc.publish("arduino" + ArduinoFBL[q] + "/relais" + RelayFBL[q] + "/action", "H", 0, False)
    if ((ToggleVButton+OnVButton+OffVButton) == 0 and RCFBLight == 1 and VButtonArray[i][z] == 1):
	printLog(info,"Change of Vbutton status!" , str(get_linenumber()))
	VButtonArray[i][z] = 0
	mqttc.publish("arduino" + str(i) + "/vbutton" + str(z) + "/status", "L", 0, True)
	if (HasPhysicFBL == 1):
	 for q in range (len(ArduinoFBL)):
	  mqttc.publish("arduino" + ArduinoFBL[q] + "/relais" + RelayFBL[q] + "/action", "L", 0, False)
	  
    if ((ToggleVButton+OnVButton+ROffVButton) == (ToggleL+OnL+OffL) and FBLight == 1 and VButtonArray[i][z] == 0):
	printLog(debug,"hoeveel lichten maar blijkbaar gelijk " + str(VButton), str(get_linenumber()))
	printLog(info,"Change of Vbutton status!" , str(get_linenumber()))
	VButtonArray[i][z] = 1
	mqttc.publish("arduino" + str(i) + "/vbutton" + str(z) + "/status", "H", 0, True)
	if (HasPhysicFBL == 1):
	 for q in range (len(ArduinoFBL)):
	  mqttc.publish("arduino" + ArduinoFBL[q] + "/relais" + RelayFBL[q] + "/action", "H", 0, False)
    if ((ToggleVButton+OnVButton+ROffVButton) != (ToggleL+OnL+OffL) and FBLight == 1 and VButtonArray[i][z] == 1):
	printLog(info,"Change of Vbutton status!" , str(get_linenumber()))
	VButtonArray[i][z] = 0
	mqttc.publish("arduino" + str(i) + "/vbutton" + str(z) + "/status", "L", 0, True)
	if (HasPhysicFBL == 1):
	 for q in range (len(ArduinoFBL)):
	  mqttc.publish("arduino" + ArduinoFBL[q] + "/relais" + RelayFBL[q] + "/action", "L", 0, False)
    if ((ToggleVButton+OnVButton+ROffVButton) > 0 and RFBLight == 1 and VButtonArray[i][z] == 0):
	VButtonArray[i][z] = 1
	mqttc.publish("arduino" + str(i) + "/vbutton" + str(z) + "/status", "H", 0, True)
	if (HasPhysicFBL == 1):
	 for q in range (len(ArduinoFBL)):
	  mqttc.publish("arduino" + ArduinoFBL[q] + "/relais" + RelayFBL[q] + "/action", "H", 0, False)
    if ((ToggleVButton+OnVButton+ROffVButton) == 0 and RFBLight == 1 and VButtonArray[i][z] == 1):
	printLog(info,"Change of Vbutton status!" , str(get_linenumber()))
	VButtonArray[i][z] = 0
	mqttc.publish("arduino" + str(i) + "/vbutton" + str(z) + "/status", "L", 0, True)
	if (HasPhysicFBL == 1):
	 for q in range (len(ArduinoFBL)):
	  mqttc.publish("arduino" + ArduinoFBL[q] + "/relais" + RelayFBL[q] + "/action", "L", 0, False)
	  	
    ToggleCheckA = ""
    ToggleCheckR = ""
    OnCheckA = ""
    OnCheckR = ""
    OffCheckA = ""
    OffCheckR = ""
    ToggleL = 0
    OnL = 0
    OffL = 0
    VButton = 0
    FBLight = 0
    RFBLight = 0
    CFBLight = 0
    RCFBLight = 0
    HasPhysicFBL = 0
    ToggleVButton = 0
    OnVButton = 0
    ROffVButton = 0
    OffVButton = 0
	  
def ButtonAction2(Arduino_number,button_pushed_int,ArrayN):
  global Custom_TIMER_LAURENT
  if Arduino_number == 2 and button_pushed_int == 9:
    Custom_TIMER_LAURENT = int(time.time())
  if  Arduino_number == 2 and button_pushed_int == 15 and Custom_TIMER_LAURENT < int(time.time()) + 1:
    Custom_TIMER_LAURENT = 0
  else:    
    ButtonAction(Arduino_number,button_pushed_int,ArrayN)
  
def ButtonAction(Arduino_number,button_pushed_int,ArrayN):
 printLog(debug,"bring the action" , str(get_linenumber()))
 Mail = ""
 Button_pushed_var = 0
 IsToggled = 0
 EverythingHigh = 0
 EverythingLow = 0
 ArduinoNumber = 0
 ArduinoNumberC = 0
 RelayCounter = 0
 RelayCheck = 0
 RelayNumber = 0
 RelayNumberC = 0
 HasDelay = 0
 RelayON = -1
 RelayOFF = -1
 END = 0
 COR = 0
 CAND = 0
 SD = 0
 CheckCOR = 0
 CheckCAND = 0
 CORstatus = 0
 ANDstatus = 0
 CANDstatus = 0
 ButtonDelay = ""
 TotalDelay = 0
 RelayOn = -1
 RelayOff = -1
 OneDelay = 0
 ButtonRelay = 0
 ButtonDimmer = 0
 DimmerValue = -2
 DimmerSpeed = -1
 DimmerArduino = 0
 DimmerRelay = 0
 DimmerFirst = 0
 RelayFirst = 0
 KodiN = ""
 KodiCheck = -1
 KodiVo = -1
 KodiPa = -1
 KodiSt = -1
 KodiPl = -1
 KodiRe = -1
 KodiPT = -1
 WPO = ""
 WPI = ""

 ButtonList = ThreeDArray[ArrayN][Arduino_number][button_pushed_int].split("|")
 for i in range (len(ButtonList)):
  if (END == 1):
   Mail = ""
   Button_pushed_var = 0
   IsToggled = 0
   EverythingHigh = 0
   EverythingLow = 0
   ArduinoNumber = 0
   ArduinoNumberC = 0
   RelayCounter = 0
   RelayCheck = 0
   RelayNumber = 0
   RelayNumberC = 0
   HasDelay = 0
   RelayON = -1
   RelayOFF = -1
   END = 0
   COR = 0
   CAND = 0
   SD = 0
   SD_Before= 0
   SD_After = 0
   CheckCOR = 0
   CheckCAND = 0
   CORstatus = 0
   ANDstatus = 0
   CANDstatus
   ButtonDelay = ""
   TotalDelay = 0
   ButtonRelay = 0
   ButtonRelayC = 0
   ButtonDimmer = 0
   DimmerValue = -2
   DimmerSpeed = -1
   DimmerArduino = ""
   DimmerRelay = ""
   DimmerFirst = 0
   RelayFirst = 0
   KodiN = ""
   KodiCheck = -1
   KodiVo = -1
   KodiPa = -1
   KodiSt = -1
   KodiPl = -1
   KodiRe = -1
   KodiPT = -1
   WPO = ""
   WPI = ""
   
  if (ButtonList[i] == "BD"):
   if (ButtonRelay == 0):
    DimmerFirst = 1
   ButtonDimmer = 1
   DimmerValue = ButtonList[i + 1]
   DimmerSpeed = ButtonList[i + 2]
   DimmerArduino = ButtonList[i + 3]
   DimmerRelay = ButtonList[i + 4]
   ButtonDelay = ButtonDelay + "BD|" + DimmerValue + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay + "|"
  if (ButtonList[i] == "M"):
   Mail = ButtonList[i + 1]
   ButtonDelay = ButtonDelay + "M|" + Mail + "|"
  if (ButtonList[i] == "WPO"):
    WPO = ButtonList[i+1]
  if (ButtonList[i] == "WPI"):
    WPI = ButtonList[i+1]
  if (ButtonList[i] == "K"):
    KodiN = ButtonList[i + 1]
	#KodiCheck = 1
    if (ButtonList[i+2] == "PL"):
      KodiPl = ButtonList[i+3]
      if (ButtonList[i+4] == "V"):
        KodiVo = ButtonList[i+5]
    if (ButtonList[i+2] == "V"):
      KodiVo = ButtonList[i+3]
    if (ButtonList[i+2] == "PA"):
      KodiPa = 1
      if (ButtonList[i+3] == "V"):
        KodiVo = ButtonList[i+4]
    if (ButtonList[i+2] == "ST"):
      KodiSt = 1
    if (ButtonList[i+2] == "RE"):
      KodiRe = 1
    if (ButtonList[i+2] == "PT"):
      KodiPT = 1
      KodiPl = ButtonList[i+3]
      if (ButtonList[i+4] == "V"):
        KodiVo = ButtonList[i+5]
	#ButtonDelay = ButtonDelay + "K|" + KodiN + "|" + RelayNumber + "|"
  if (ButtonList[i] == "R" and COR == 0 and CAND == 0):
   if (ButtonDimmer == 0):
    RelayFirst = 1
   ButtonRelay = 1
   ArduinoNumber = ButtonList[i + 1]
   RelayNumber = ButtonList[i + 2]
   ButtonDelay = ButtonDelay + "R|" + ArduinoNumber + "|" + RelayNumber + "|"
  if (ButtonList[i] == "R" and (COR == 1 or CAND == 1)):
   ButtonRelayC = 1
   ArduinoNumberC = ButtonList[i + 1]
   RelayNumberC = ButtonList[i + 2]
   ButtonDelay = ButtonDelay + "R|" + ArduinoNumberC + "|" + RelayNumberC + "|"
  if (ButtonList[i] == "D"):
   HasDelay = int(ButtonList[i + 1])
  if (ButtonList[i] == "On"):
   RelayON = int(ButtonList[i + 1])
   ButtonDelay = ButtonDelay + "On|" + str(RelayON) + "|"
  if (ButtonList[i] == "T"):
   printLog(info,"toggled ? "+str(ButtonList[i]) , str(get_linenumber()))
   IsToggled = 1
   ButtonDelay = ButtonDelay + "T|"
  if (ButtonList[i] == "Off"):
   RelayOFF = int(ButtonList[i + 1])
   ButtonDelay = ButtonDelay + "Off|" + str(RelayOFF) + "|"
  if (ButtonList[i] == "CO"):
   COR = 1
   ButtonDelay = ButtonDelay + "CO|"
  if (ButtonList[i] == "CA"):
   CAND = 1
   ButtonDelay = ButtonDelay + "CA|"
  if ("SD" in ButtonList[i]):
   SD = 1
   adjustment = ButtonList[i].split(';')
   SD_Before= adjustment[1]
   SD_After = adjustment[2]
   ButtonDelay = ButtonDelay + ButtonList[i] +"|"
  if (ButtonList[i] == "E"):
   END = 1
   ButtonDelay = ButtonDelay + "E|"
   if (HasDelay == 0 or OneDelay == 1):
    if (COR > 0 or CAND > 0):
     if (COR > 0):
      if (SD > 0):
       CORstatus = CORstatus + 1
       if (SunDown(str(SD_Before),str(SD_After)) == "true"):
        CheckCOR = CheckCOR + 1
      if (ArduinoNumberC != 0):
       CORstatus = CORstatus + 1
       if (RelayChecker(ArduinoNumberC,RelayNumberC,0) == "true"):
        CheckCOR = CheckCOR + 1
      if (WPI):
        WPINumber = WPI.split(";")
        for i in range (len(WPINumber)):
          if (checkOwntracks(WPINumber[i]),"WPI"):
            CheckCOR = CheckCOR + 1
      if (WPO):
        WPONumber = WPO.split(";")
        for i in range (len(WPONumber)):
          if (checkOwntracks(WPONumber[i]),"WPO"):
            CheckCOR = CheckCOR + 1
     if (CAND > 0):
      if (SD > 0):
       CANDstatus = CANDstatus + 1
       if (SunDown(str(SD_Before),str(SD_After)) == "true"):
        CheckCAND = CheckCAND + 1
      if (ArduinoNumberC != 0):
       CANDstatus = CANDstatus + 1
       if (RelayChecker(ArduinoNumberC,RelayNumberC,1) == "true"):
        CheckCAND = CheckCAND + 1
      if (WPI):
        WPINumber = WPI.split(";")
        for i in range (len(WPINumber)):
          CANDstatus = CANDstatus + 1
          if (checkOwntracks(WPINumber[i]),"WPI"):
            CheckCAND = CheckCAND + 1
      if (WPO):
        WPONumber = WPO.split(";")
        for i in range (len(WPONumber)):
          CANDstatus = CANDstatus + 1
          if (checkOwntracks(WPONumber[i]),"WPO"):
            CheckCAND = CheckCAND + 1
     if (CheckCOR > 0 or (CANDstatus > 0 and CANDstatus == CheckCAND)):
      if (IsToggled > 0):
       ArduinoList = ArduinoNumber.split(";")
       RelayList = RelayNumber.split(";")
       for b in range (len(ArduinoList)):
        if (RelayStatus[int(ArduinoList[b])][int(RelayList[b])] == 0 and EverythingHigh == 0 and EverythingLow == 0):
         EverythingHigh = 1
         printLog(debug,"arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action/H" , str(get_linenumber()))
         #mqttc.publish("arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action", "H", 0, False)
        if (RelayStatus[int(ArduinoList[b])][int(RelayList[b])] == 1 and EverythingHigh == 0 and EverythingLow == 0):
         EverythingLow = 1
         printLog(debug,"arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action/L" , str(get_linenumber()))
         #mqttc.publish("arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action", "L", 0, False)
        if (EverythingLow == 1):
         printLog(debug,"arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action/L" , str(get_linenumber()))
         mqttc.publish("arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action", "L", 0, False)
        if (EverythingHigh == 1):
         printLog(debug,"arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action/H" , str(get_linenumber()))
         mqttc.publish("arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action", "H", 0, False)
      if (RelayON > -1):
       ArduinoList = ArduinoNumber.split(";")
       RelayList = RelayNumber.split(";")
       for c in range (len(ArduinoList)):
        RelayOnTimer[int(ArduinoList[c])][int(RelayList[c])] = int(time.time()) + RelayON
        printLog(debug,"arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action/L" , str(get_linenumber()))
        mqttc.publish("arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action", "L", 0, False)
      if (RelayOFF > 0):
       ArduinoList = ArduinoNumber.split(";")
       RelayList = RelayNumber.split(";")
       for c in range (len(ArduinoList)):
        RelayOffTimer[int(ArduinoList[c])][int(RelayList[c])] = int(time.time()) + RelayOFF
        printLog(debug,"arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action/H" , str(get_linenumber()))
        mqttc.publish("arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action", "H", 0, False)
      if (RelayOFF == 0):
       ArduinoList = ArduinoNumber.split(";")
       RelayList = RelayNumber.split(";")
       for c in range (len(ArduinoList)):
        RelayOffTimer[int(ArduinoList[c])][int(RelayList[c])] = int(time.time()) + RelayOFF
        printLog(debug,"arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action/L" , str(get_linenumber()))
        mqttc.publish("arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action", "L", 0, False)

      if (Mail != ""):
       MailSend(Mail)
    else: 
     if (KodiN != ""):
      KodiList = KodiN.split(";")
     if (KodiPl > -1):
      for x in range (len(KodiList)):
       mqttc.publish("kodi" + KodiList[x] + "/command/play",GetChannel(KodiPl), 0, True)
     if (str(KodiVo) != "-1"):
      for x in range (len(KodiList)):
       mqttc.publish("kodi" + KodiList[x] + "/command/volume",KodiVo, 0, True)
     if (KodiPa > -1):
      for x in range (len(KodiList)):
       mqttc.publish("kodi" + KodiList[x] + "/command/playbackstate","pause", 0, True)
     if (KodiSt > -1):
      for x in range (len(KodiList)):
       mqttc.publish("kodi" + KodiList[x] + "/command/playbackstate","stop", 0, True)
     if (KodiRe > -1):
      for x in range (len(KodiList)):
       mqttc.publish("kodi" + KodiList[x] + "/command/resume", 0, True)
     if (KodiPT > -1):
      for x in range (len(KodiList)):
       if (KodiStatus[x] == 0):
        mqttc.publish("kodi" + KodiList[x] + "/command/play",GetChannel(KodiPl), 0, True)
       if (KodiStatus[x] == 1):
        mqttc.publish("kodi" + KodiList[x] + "/command/playbackstate","stop", 0, True)
       if (KodiStatus[x] == 2):
        mqttc.publish("kodi" + KodiList[x] + "/command/playbackstate","resume", 0, True)
     if (IsToggled > 0):
      if (RelayFirst > 0):
       ArduinoList = ArduinoNumber.split(";")
       RelayList = RelayNumber.split(";")
       for b in range (len(ArduinoList)):
        if (RelayStatus[int(ArduinoList[b])][int(RelayList[b])] == 0 and EverythingHigh == 0 and EverythingLow == 0):
         EverythingHigh = 1
        if (RelayStatus[int(ArduinoList[b])][int(RelayList[b])] == 1 and EverythingHigh == 0 and EverythingLow == 0):
         EverythingLow = 1
      if (DimmerFirst > 0):
       ArduinoDimmerList = DimmerArduino.split(";")
       RelayDimmerList = DimmerRelay.split(";")
       for b in range (len(ArduinoDimmerList)):
        if (RelayStatus[int(ArduinoDimmerList[b])][int(RelayDimmerList[b])] == 0 and EverythingHigh == 0 and EverythingLow == 0):
         EverythingHigh = 1
        if (RelayStatus[int(ArduinoDimmerList[b])][int(RelayDimmerList[b])] == 1 and EverythingHigh == 0 and EverythingLow == 0):
         EverythingLow = 1
      if (EverythingLow == 1):
       if (ButtonRelay > 0):
        ArduinoList = ArduinoNumber.split(";")
        RelayList = RelayNumber.split(";")
        for b in range (len(ArduinoList)):
	 if (DimmerInAction[int(ArduinoList[b])][int(RelayList[b])] == 1):
	  DimmerInAction[int(ArduinoList[b])][int(RelayList[b])] = 2
         printLog(debug,"arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action/L" , str(get_linenumber()))
         mqttc.publish("arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action", "L", 0, False)
       if (ButtonDimmer > 0):
        ButtonDimmerOff(Arduino_number,button_pushed_int,DimmerValue,DimmerArduino,DimmerRelay,DimmerSpeed)

      if (EverythingHigh == 1):
       if (ButtonRelay > 0):
        ArduinoList = ArduinoNumber.split(";")
        RelayList = RelayNumber.split(";")       
        for b in range (len(ArduinoList)):
	 if (DimmerInAction[int(ArduinoList[b])][int(RelayList[b])] == 1):
	  DimmerInAction[int(ArduinoList[b])][int(RelayList[b])] = 2
         printLog(debug,"arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action/H" , str(get_linenumber()))
         mqttc.publish("arduino" + ArduinoList[b] + "/relais" + RelayList[b] + "/action", "H", 0, False)
       if (ButtonDimmer > 0):
        ButtonDimmerOn(Arduino_number,button_pushed_int,DimmerValue,DimmerArduino,DimmerRelay,DimmerSpeed)

     if (RelayON > -1):
      if (ButtonRelay > 0):
       ArduinoList = ArduinoNumber.split(";")
       RelayList = RelayNumber.split(";")
       for c in range (len(ArduinoList)):
        if (RelayON == 0):
	 if (DimmerInAction[int(ArduinoList[c])][int(RelayList[c])] == 1):
	  DimmerInAction[int(ArduinoList[c])][int(RelayList[c])] = 2
         printLog(debug,"arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action/H" , str(get_linenumber()))
         mqttc.publish("arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action", "H", 0, False)
        else:
         if (DimmerInAction[int(ArduinoList[c])][int(RelayList[c])] == 1):
	  DimmerInAction[int(ArduinoList[c])][int(RelayList[c])] = 2
         RelayOnTimer[int(ArduinoList[c])][int(RelayList[c])] = int(time.time()) + RelayON
         printLog(debug,"arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action/L" , str(get_linenumber()))
         mqttc.publish("arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action", "L", 0, False)
      if (ButtonDimmer > 0):
       if (RelayON == 0):
        ButtonDimmerOn(Arduino_number,button_pushed_int,DimmerValue,DimmerArduino,DimmerRelay,DimmerSpeed)
       else:
        ArduinoDimmerList = DimmerArduino.split(";")
	RelayDimmerList = DimmerRelay.split(";")        
	for d in range (len(ArduinoDimmerList)):
         DimmerOnTimerValue[int(ArduinoDimmerList[c])][int(RelayDimmerList[c])] = Arduino_number + "|" + button_pushed_int + "|" + DimmerValue + "|" + DimmerArduino + "|" + DimmerRelay + "|" + DimmerSpeed
         DimmerOnTimer[int(ArduinoDimmerList[c])][int(RelayDimmerList[c])] = int(time.time()) + RelayON
     if (RelayOFF > -1):
      if (ButtonRelay > 0):
       ArduinoList = ArduinoNumber.split(";")
       RelayList = RelayNumber.split(";")
       for c in range (len(ArduinoList)):
        if (RelayOFF == 0):
         printLog(debug,"arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action/L" , str(get_linenumber()))
         mqttc.publish("arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action", "L", 0, False)
        else:
         RelayOffTimer[int(ArduinoList[c])][int(RelayList[c])] = int(time.time()) + RelayOFF
         printLog(debug,"arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action/H" , str(get_linenumber()))
         mqttc.publish("arduino" + ArduinoList[c] + "/relais" + RelayList[c] + "/action", "H", 0, False)
      if (ButtonDimmer > 0):
       if (RelayOFF == 0):
        ButtonDimmerOff(Arduino_number,button_pushed_int,DimmerValue,DimmerArduino,DimmerRelay,DimmerSpeed)
       else:
        ArduinoDimmerList = DimmerArduino.split(";")
	RelayDimmerList = DimmerRelay.split(";")        
	for d in range (len(ArduinoDimmerList)):
         DimmerOffTimerValue[int(ArduinoDimmerList[c])][int(RelayDimmerList[c])] = Arduino_number + "|" + button_pushed_int + "|" + DimmerValue + "|" + DimmerArduino + "|" + DimmerRelay + "|" + DimmerSpeed
         DimmerOffTimer[int(ArduinoDimmerList[c])][int(RelayDimmerList[c])] = int(time.time()) + RelayOFF
     if (Mail != ""):
      MailSend(Mail)
     printLog(debug,"ButtonDimmer: " + str(ButtonDimmer) + "| ButtonTimerArray[Arduino_number= " + str(Arduino_number) + " ][button_pushed_int= " +str(button_pushed_int) + "]: " + str(ButtonTimerArray[Arduino_number][button_pushed_int]) , str(get_linenumber()))
     printLog(debug,"ButtonValue: " + str(DimmerValue) + " EverythingHigh: " + str(EverythingHigh), str(get_linenumber()))
     if (ButtonDimmer == 1 and ButtonTimerArray[Arduino_number][button_pushed_int] == 2):
      printLog(debug,"ButtonDimmer RT -> RealTime function used" , str(get_linenumber()))
      ArduinoDimmerList = DimmerArduino.split(";")
      RelayDimmerList = DimmerRelay.split(";")
      for f in range (0,1):
       if (RelayDimmerDirection[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 0):
        if (RelayStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 1):
         if (RelayDimmerStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 0):
	  for z in range (len(ArduinoDimmerList)):
	   RelayDimmerValue[int(ArduinoDimmerList[z])][int(RelayDimmerList[z])] = 100	  
	  RelayDimmerDirection[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] = 1
          ButtonDimmerAction[Arduino_number][button_pushed_int] =  "RTOFF|" + "100" + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay
         if (RelayDimmerStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 1):
	  RelayDimmerDirection[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] = 1
          ButtonDimmerAction[Arduino_number][button_pushed_int] =  "RTOFF|" + str(RealTimeDimmerValue[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])]) + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay
	if (RelayStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 0):
	 for z in range (len(ArduinoDimmerList)):
	  RelayDimmerValue[int(ArduinoDimmerList[z])][int(RelayDimmerList[z])] = 0	  
	 RelayDimmerDirection[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] = 0
	 ButtonDimmerAction[Arduino_number][button_pushed_int] =  "RTON|" + "0" + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay
       else:
        if (RelayStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 1):
         if (RelayDimmerStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 1):
	  RelayDimmerDirection[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] = 0
          ButtonDimmerAction[Arduino_number][button_pushed_int] =  "RTON|" + str(RealTimeDimmerValue[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])]) + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay
         if (RelayDimmerStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 0):
	  for z in range (len(ArduinoDimmerList)):
	   RelayDimmerValue[int(ArduinoDimmerList[z])][int(RelayDimmerList[z])] = 100	 
	  RelayDimmerDirection[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] = 1
          ButtonDimmerAction[Arduino_number][button_pushed_int] =  "RTOFF|" + str(RealTimeDimmerValue[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])]) + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay
        if (RelayStatus[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] == 0):
	 RelayDimmerDirection[int(ArduinoDimmerList[f])][int(RelayDimmerList[f])] = 0
	 for z in range (len(ArduinoDimmerList)):
	  RelayDimmerValue[int(ArduinoDimmerList[z])][int(RelayDimmerList[z])] = 0
	 ButtonDimmerAction[Arduino_number][button_pushed_int] =  "RTON|" + "0" + "|" + DimmerSpeed + "|" + DimmerArduino + "|" + DimmerRelay

   
   else:
    ThreeDArray[1][Arduino_number][button_pushed_int] = ButtonDelay
    TotalDelay = int(time.time()) + int(HasDelay)
    DelayTimer[Arduino_number][button_pushed_int] = TotalDelay
    OneDelay = 1

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect
# Uncomment to enable debug messages
#mqttc.on_log = on_log

try:	
	cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	query = ("SELECT actie,arduino,pin FROM Core_vButtonDB")
	printLog(info,"Query "+query, str(get_linenumber())) 
	cursor.execute(query)


	for (actie, arduino, pin) in cursor:
		if actie is None:
			actie = "0"
		ThreeDArray[0][int(arduino)][int(pin)] = actie

except Exception as e:
	printLog(info,e, str(get_linenumber())) 
finally:		
	cursor.close()	
	cnx.close()
		

for x in range(0, int(number_of_arduino)):
	for y in range(0, 16):
		printLog(info,"arduino: " + str(x) + " ,pin: " + str(y) + " ,actie: " + str(ThreeDArray[0][x][y]) , str(get_linenumber()))
		
running = True
while running:
        try:
				mqttc.connect(MQTT_ip_address,int(MQTT_port), 60)
				running = False
        except:
                printLog(info,"Sleep" , str(get_linenumber()))
                time.sleep(5)
printLog(info,"Connected" , str(get_linenumber()))



for g in range (len(RelayStatus)):
 mqttc.subscribe("arduino" + str(g) +"/radio/volume", 0)
 #printLog(info,"Subscribe on arduino" + str(g) + "/radio/volume" , str(get_linenumber()))
 mqttc.subscribe("arduino" + str(g) +"/radio/channel", 0)
 for h in range (len(RelayStatus[g])):
  #mqttc.publish("arduino" + str(g) +"/relais" + str(h) + "/action","",0,True);
  if "|W|" in ThreeDArray[0][g][h]:
   ButtonList = ThreeDArray[0][g][h].split("|")
   for i in range (len(ButtonList)):
    if (ButtonList[i] == "R"):
     ArduinoNumber = ButtonList[i + 1]
     RelayNumber = ButtonList[i + 2]
   ArduinoList = ArduinoNumber.split(";")
   RelayList = RelayNumber.split(";")
   for c in range (len(ArduinoList)):
 	printLog(info,"Bewegingsmelder down: publish: arduino" + str(ArduinoList[c]) + "/relais" + str(RelayList[c]) + "/action/L" , str(get_linenumber()))
	mqttc.publish("arduino" + str(ArduinoList[c]) + "/relais" + str(RelayList[c]) + "/action", "L", 0, False)   
  mqttc.subscribe("arduino" + str(g) +"/button" + str(h) + "/status", 0)
  mqttc.subscribe("arduino" + str(g) +"/relais" + str(h) + "/status", 0)
  mqttc.subscribe("arduino" + str(g) +"/dimmer" + str(h) + "/status", 0)

mqttc.subscribe(CoreService + "/service/restart", 0)

while True:
 mqttc.loop(timeout=0.1, max_packets=1)
 #printLog(debug,"Timestampcheck", str(get_linenumber()))
 for f in range (len(ButtonMessage)):
  for g in range (len(ButtonMessage[f])):
     if (ButtonMessage[f][g] == "L"):
      printLog(debug,"Button Low ? " + str(ButtonMessage[f][g]),str(get_linenumber()))
      if (WaitTimer[f][g] > 0):
       printLog(debug,"So we will wait "+str(WaitTimer[f][g]) , str(get_linenumber()))
       WaitTimer[f][g] = WaitTimer[f][g] - 1
      if (WaitTimer[f][g] == 0):
       ExtendOffTimer(f,g,0)
       WaitTimer[f][g] = 5
       printLog(debug,"Renew Relay Status" , str(get_linenumber()))
      if (WaitTime[f][g] == 0):
       WaitTime[f][g] = int(time.time()) + WaitBA(f,g,0)
      if (WaitTime[f][g] != 0 and int(time.time()) >= WaitTime[f][g] and ButtonMessage[f][g] == "L"):
       printLog(debug,"make him high" , str(get_linenumber()))
       ButtonPushed[f][g] = 1
       ButtonMessage[f][g] = "H"
       WaitTimer[f][g] = 0
       WaitTime[f][g] = 0
     else:
      WaitTimer[f][g] = 0
      WaitTime[f][g] = 0
 for i in range (len(RelayOnTimer)):
  for j in range (len(RelayOnTimer[i])):
   if (RelayOnTimer[i][j] > -1 and int(time.time()) >= RelayOnTimer[i][j]):
    printLog(debug,"publish: arduino" + str(i) + "/relais" + str(j) + "/action/H" , str(get_linenumber()))
    mqttc.publish("arduino" + str(i) + "/relais" + str(j) + "/action", "H", 0, False)
    RelayOnTimer[i][j] = -1
 for i in range (len(RelayOffTimer)):
  for j in range (len(RelayOffTimer[i])):
   if (RelayOffTimer[i][j] > -1 and int(time.time()) >= RelayOffTimer[i][j]):
    printLog(debug,"publish: arduino" + str(i) + "/relais" + str(j) + "/action/L" , str(get_linenumber()))
    mqttc.publish("arduino" + str(i) + "/relais" + str(j) + "/action", "L", 0, False)
    RelayOffTimer[i][j] = -1
    
 for i in range (len(DimmerOnTimer)):
  for j in range (len(DimmerOnTimer[i])):
   if (DimmerOnTimer[i][j] > -1 and int(time.time()) >= DimmerOnTimer[i][j]):
    printLog(debug,"arduino Dimmer timer" + str(i) + "/relais" + str(j) + "/action/H" , str(get_linenumber()))
    DimmerOnTimerValueList = DimmerOnTimerValue[i][j].split("|")
    DimmerOnTimer[i][j] = -1
    ButtonDimmerOn(DimmerOnTimerValueList[0],DimmerOnTimerValueList[1],DimmerOnTimerValueList[2],DimmerOnTimerValueList[3],DimmerOnTimerValueList[4],DimmerOnTimerValueList[5])
 for i in range (len(DimmerOffTimer)):
  for j in range (len(DimmerOffTimer[i])):
   if (DimmerOffTimer[i][j] > -1 and int(time.time()) >= DimmerOffTimer[i][j]):
    printLog(debug,"arduino Dimmer timer" + str(i) + "/relais" + str(j) + "/action/L" , str(get_linenumber()))
    DimmerOffTimerValueList = DimmerOffTimerValue[i][j].split("|")
    DimmerOffTimer[i][j] = -1
    ButtonDimmerOff(DimmerOffTimerValueList[0],DimmerOffTimerValueList[1],DimmerOffTimerValueList[2],DimmerOffTimerValueList[3],DimmerOffTimerValueList[4],DimmerOffTimerValueList[5])

 for k in range (len(DelayTimer)):
  for l in range (len(DelayTimer[k])):
   if (DelayTimer[k][l] > 0 and int(time.time()) >= DelayTimer[k][l]):
    printLog(debug,DelayButton[k][l] , str(get_linenumber()))
    DelayTimer[k][l] = 0
    ButtonAction2(k,l,1)
	
 for w in range (len(ButtonTimerArray)):
  for x in range (len(ButtonTimerArray[w])):
   if (ButtonTimerArray[w][x] == 1):
    if (ButtonOffsetArray[w][x] <= int(time.time())):
      ButtonSecondAction = ThreeDArray[0][w][x].split("BTF")
      ThreeDArray[3][w][x] = ButtonSecondAction[0]
      ButtonTimerArray[w][x] = 2
      ButtonAction2(w,x,3)
      
 for s in range (len(ButtonDimmerAction)):
  for d in range (len(ButtonDimmerAction[s])):
   if (ButtonDimmerAction[s][d] != 0):
    DimmerArduinoTwo = 0
    DimmerRelayTwo = 0
    ButtonDimmerA = ButtonDimmerAction[s][d].split("|")
    RealTimeButton = ButtonDimmerA[0]
    DimmerValue = int(ButtonDimmerA[1])
    if (DimmerValue == 0):
     DimmerValue = 100
    DimmerSpeed = int(ButtonDimmerA[2])
    DimmerArduino = ButtonDimmerA[3]
    DimmerRelay = ButtonDimmerA[4]
    TimeStamp = int(round(time.time() * 1000))
    OffsetNumber = 100000/(5 * int(DimmerSpeed))
    printLog(debug,"DimmerValue :" + str(DimmerValue) + " DimmerSpeed :" + str(DimmerSpeed) + " DimmerArduino :" + str(DimmerArduino) + " DimmerRelay :" + str(DimmerRelay) + " DimmerOffset :" + str(OffsetNumber), str(get_linenumber()))
    ArduinoDimmerList = DimmerArduino.split(";")
    RelayDimmerList = DimmerRelay.split(";")
    printLog(debug,"ButtonDimmerTimer :" + str(ButtonDimmerTimer[s][d]) + " millis :" + str(TimeStamp) , str(get_linenumber()))
    if (int(ButtonDimmerTimer[s][d]) <= TimeStamp):
     ButtonDimmerTimer[s][d] = TimeStamp + 200
     printLog(debug,"Timestamp :" + str(TimeStamp), str(get_linenumber()))
     printLog(debug,"Check ButtonDimmerTimer :" + str(ButtonDimmerTimer[s][d]) + "Check DimmerValue :" + str(DimmerValue), str(get_linenumber()))
     
     if (RealTimeButton == "ON"):
      for t in range (len(ArduinoDimmerList)):
       printLog(debug,"PUT relay ON with following variables: Dimmervalue = " + str(DimmerValue) + " DimmerSpeed = " + str(DimmerSpeed) + " DimmerArduino = " + str(DimmerArduino) + " DimmerRelay = " + str(DimmerRelay) , str(get_linenumber()))  
       if (RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] != DimmerValue):
        if (DimmerInAction[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] == 0):
	 DimmerInAction[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] = 1
        printLog(debug,"OFFSET = RelayDimmerValue(" + str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) + ") + Offset(" + str(OffsetNumber) + ")" , str(get_linenumber()))
	RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] = int(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) + OffsetNumber  
	if (RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] > DimmerValue):
	 RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] = DimmerValue	
	if (DimmerInAction[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] == 1):   
 	 mqttc.publish("arduino" + str(ArduinoDimmerList[t]) + "/dimmer" + str(RelayDimmerList[t]) + "/value", str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]), 0, True)
	 printLog(debug,"publish arduino" + str(ArduinoDimmerList[t]) + "/dimmer" + str(RelayDimmerList[t]) + "/value " + str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) , str(get_linenumber()))   
	else:
	 for g in range (len(ArduinoDimmerList)):
	  if (g != t):
	   DimmerArduinoTwo += ArduinoDimmerList[g] if DimmerArduinoTwo == "" else ";" + ArduinoDimmerList[g]
	   DimmerRelayTwo += RelayDimmerList[g] if DimmerRelayTwo == "" else ";" + RelayDimmerList[g]
	  else:
	   DimmerInAction[int(ArduinoDimmerList[g])][int(RelayDimmerList[g])] = 0
	 if (DimmerArduinoTwo == 0):
	  ButtonDimmerAction[s][d] = 0
	 else:
	  ButtonDimmerAction[s][d] = RealTimeButton + "|" + DimmerValue + "|" + DimmerArduinoTwo + "|" + DimmerRelayTwo
       else:
        ButtonDimmerAction[s][d] = 0
	ButtonTimerArray[s][d] = 0
	for j in range (len(ArduinoDimmerList)):
	 DimmerInAction[int(ArduinoDimmerList[j])][int(RelayDimmerList[j])] = 0

     if (RealTimeButton == "OFF"):
      for t in range (len(ArduinoDimmerList)):
       printLog(debug,"PUT relay OFF" , str(get_linenumber()))
       if (RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] != 0):
        if (DimmerInAction[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] == 0):
	 DimmerInAction[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] = 1
        printLog(debug,"OFFSET = RelayDimmerValue(" + str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) + ") - Offset(" + str(OffsetNumber) + ")" , str(get_linenumber()))
        RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] = int(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) - OffsetNumber
	if (RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] < 0):
	 RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] = 0
	if (DimmerInAction[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] == 1):   	   
	 mqttc.publish("arduino" + str(ArduinoDimmerList[t]) + "/dimmer" + str(RelayDimmerList[t]) + "/value", str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]), 0, True)
	 printLog(debug,"arduino" + str(ArduinoDimmerList[t]) + "/dimmer" + str(RelayDimmerList[t]) + "/value " + str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) , str(get_linenumber()))   
	else:
	 for g in range (len(ArduinoDimmerList)):
	  if (g != t):
	   DimmerArduinoTwo += ArduinoDimmerList[g] if DimmerArduinoTwo == "" else ";" + ArduinoDimmerList[g]
	   DimmerRelayTwo += RelayDimmerList[g] if DimmerRelayTwo == "" else ";" + RelayDimmerList[g]
	  else:
	   DimmerInAction[int(ArduinoDimmerList[g])][int(RelayDimmerList[g])] = 0
	 if (DimmerArduinoTwo == 0):
	  ButtonDimmerAction[s][d] = 0
	 else:
	  ButtonDimmerAction[s][d] = RealTimeButton + "|" + DimmerValue + "|" + DimmerArduinoTwo + "|" + DimmerRelayTwo
       else:
        mqttc.publish("arduino" + str(ArduinoDimmerList[t]) + "/dimmer" + str(RelayDimmerList[t]) + "/value", str(0), 0, True)
        ButtonDimmerAction[s][d] = 0
	ButtonTimerArray[s][d] = 0
	for j in range (len(ArduinoDimmerList)):
	 DimmerInAction[int(ArduinoDimmerList[j])][int(RelayDimmerList[j])] = 0
      
     if (RealTimeButton == "RTON" and ButtonTimerArray[s][d] == 2):
      for t in range (len(ArduinoDimmerList)):
       printLog(debug,"PUT relay ON in realtime" , str(get_linenumber()))
       if (RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] != 100):
        printLog(debug,"OFFSET = RelayDimmerValue(" + str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) + ") + Offset(" + str(OffsetNumber) + ")" , str(get_linenumber()))
        RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] = int(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) + OffsetNumber  
	if (RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] > 100):
	 RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] = 100	   
	mqttc.publish("arduino" + str(ArduinoDimmerList[t]) + "/dimmer" + str(RelayDimmerList[t]) + "/value", str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]), 0, True)
	printLog(debug,"publish arduino" + str(ArduinoDimmerList[t]) + "/dimmer" + str(RelayDimmerList[t]) + "/value " + str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) , str(get_linenumber()))   
       else:
        ButtonDimmerAction[s][d] = 0
	ButtonTimerArray[s][d] = 0
	
     if (RealTimeButton == "RTOFF" and ButtonTimerArray[s][d] == 2):
      for t in range (len(ArduinoDimmerList)):
       printLog(debug,"PUT relay OFF in realtime" , str(get_linenumber()))
       if (RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] != 0):
        printLog(debug,"OFFSET = RelayDimmerValue(" + str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) + ") - Offset(" + str(OffsetNumber) + ")" , str(get_linenumber()))
        RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] = int(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) - OffsetNumber  
	if (RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] < 0):
	 RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])] = 0	   
	mqttc.publish("arduino" + str(ArduinoDimmerList[t]) + "/dimmer" + str(RelayDimmerList[t]) + "/value", str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]), 0, True)
	printLog(debug,"publish arduino" + str(ArduinoDimmerList[t]) + "/dimmer" + str(RelayDimmerList[t]) + "/value " + str(RelayDimmerValue[int(ArduinoDimmerList[t])][int(RelayDimmerList[t])]) , str(get_linenumber()))   
       else:
        ButtonDimmerAction[s][d] = 0
	ButtonTimerArray[s][d] = 0
	
