#Version 1.1
import sys
sys.path.append('/var/www/html/modules/libraries')
import schedule
import time
import pytz
from astral import *
import datetime
import os
import subprocess
import mysql.connector
import threading
import paho.mqtt.client as mqtt
import random

file = open('/var/www/html/config.php', 'r')


for line in file:
	if "db_name" in line: MySQL_database = line.split('"')[3]
	elif "db_user" in line: MySQL_username = line.split('"')[3]
	elif "db_password" in line: MySQL_password = line.split('"')[3]
	elif "db_host" in line: MySQL_host = line.split('"')[3]

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
	elif Setting == "Location":
		city_name = value
cursor.close()
cnx.close()		
	
debug = "DEBUG"
info = "INFO"
TimerService = "timer"
	
def printLog(level,message):
	if (level.upper() == Loglevel.upper() or (level.upper() == info.upper() and Loglevel.upper() == debug.upper())):
		print(level +"["+str(datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')) + "]: " +str(message))

printLog(info,"timer started!")

printLog(debug,MySQL_database)
printLog(debug,MySQL_username)
printLog(debug,MySQL_password)
printLog(debug,MySQL_host)
printLog(debug,MQTT_ip_address)
printLog(debug,MQTT_port)
printLog(debug,Loglevel)
printLog(debug,TimerService)


EverydayList = []
MondayList = []
TuesdayList = []
WednesdayList = []
ThursdayList = []
FridayList = []
SaturdayList = []
SundayList = []



def restart():			
	printLog(info,TimerService +" service has been restarted by the script")
	subprocess.call(["sudo", "supervisorctl", "restart" ,TimerService])  

def on_connect(mqttc, obj, rc):
	printLog(debug,"rc: "+str(rc))

def on_message(mqttc, obj, msg):
	restart();

def on_publish(mqttc, obj, mid):
	printLog(debug,"mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    printLog(debug,"Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    printLog(debug,string)
	
def on_disconnect(client, userdata, rc):
	logger.printLog(info, "on_disconnect!", str(logger.get_linenumber()))
	exit()	

def calcSunTime(type,adjustment):
	a = Astral()
	date = datetime.date.today()
	city = a[city_name]
	# sunriseTmp = a.sunrise_utc(date,50.813826,5.008213)
	sun = city.sun(date, local=True)
	strSunRiseMin = "0" + str(sun[type].minute)
	strSunRiseHour = "0" + str(sun[type].hour)
	
	Minutes = int(strSunRiseHour[-2:])*60 + int(strSunRiseMin[-2:])
	DefMinutes = Minutes + adjustment
	CalcHours = DefMinutes // 60
	CalcMinutes = DefMinutes - CalcHours * 60
	printLog(debug,"set_sunrise() "+"%d:%02d" % (CalcHours, CalcMinutes))
	return "%d:%02d" % (CalcHours, CalcMinutes)

def setAdjustment(Time):
	adjustment = 0
	if "+" in Time:
		tmp,adjustment = Time.split("+")
	elif "-" in Time:
		tmp,adjustment = Time.split("-")
		adjustment = -int(adjustment);
	printLog(debug,"setAdjustment() "+str(adjustment))
	return int(adjustment)

	
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
                printLog(info,"Sleep")
                time.sleep(5)
printLog(info,"Connected")

mqttc.publish("StatsService/service/cleanup", 0, False)

mqttc.subscribe(TimerService + "/service/restart", 0)


cnx = mysql.connector.connect(host=MySQL_host,user=MySQL_username,password=MySQL_password,database=MySQL_database)
cursor = cnx.cursor()


cursor.execute("SELECT Timer_Actions.Naam, Time,Time2, Random, Timer_Day,Core_vButtonDB.arduino, Core_vButtonDB.pin FROM Timer_Actions inner join Core_vButtonDB on Timer_Actions.Core_vButton_id = Core_vButtonDB.id WHERE enabled = 1")
for (Naam, Time,Time2,Random, Timer_Day,arduino,pin) in cursor:
	
	if "sunrise" in Time:
		Time = calcSunTime('sunrise',setAdjustment(Time))
	elif "sunset"in Time:
		Time = calcSunTime('sunset',setAdjustment(Time))
	
	if "sunrise" in Time2:
		Time2 = calcSunTime('sunrise',setAdjustment(Time2))
	elif "sunset"in Time2:
		Time2 = calcSunTime('sunset',setAdjustment(Time2))	
	
	if Random == 1:
		hour1,min1 = Time.split(":")
		hour2,min2 = Time2.split(":")
		Minuts1 = (int(hour1) * 60) + int(min1)
		Minuts2 = (int(hour2) * 60) + int(min2)
		if Minuts1 > Minuts2:
			TmpMinuts2 = Minuts2
			Minuts2 = Minuts1
			Minuts1 = TmpMinuts2
			
		rdmmin = random.randrange(Minuts1, Minuts2) 
		hours = rdmmin // 60
		minutes = rdmmin - hours * 60

		Time = "%d:%02d" % (hours, minutes)
	
	if Timer_Day == "1|2|3|4|5|6|7":
			EverydayList.append(str(Naam) + "|" + str(Time) + "|" + str(arduino) + "|" + str(pin))
	else:
		Days = Timer_Day.split("|")
		for Day in Days:	
			if Day == "1":
				MondayList.append(str(Naam) + "|" + str(Time) + "|" + str(arduino) + "|" + str(pin))
			elif Day == "2":
				TuesdayList.append(str(Naam) + "|" + str(Time) + "|" + str(arduino) + "|" + str(pin))
			elif Day == "3":
				WednesdayList.append(str(Naam) + "|" + str(Time) + "|" + str(arduino) + "|" + str(pin))
			elif Day == "4":
				ThursdayList.append(str(Naam) + "|" + str(Time) + "|" + str(arduino) + "|" + str(pin))
			elif Day == "5":
				FridayList.append(str(Naam) + "|" + str(Time) + "|" + str(arduino) + "|" + str(pin))
			elif Day == "6":
				SaturdayList.append(str(Naam) + "|" + str(Time) + "|" + str(arduino) + "|" + str(pin))
			elif Day == "7":
				SundayList.append(str(Naam) + "|" + str(Time) + "|" + str(arduino) + "|" + str(pin))

cursor.close()
cnx.close()

def Time():
	printLog(debug,"Time() "+"[" + str(datetime.datetime.now()) + "] ")
	return "[" + str(datetime.datetime.now()) + "] "

	
def run_threaded(func, parm):
     threading.Thread(target=func, args=parm).start()
			
def Toggle(Naam,Arduino,Pin):
			mqttc.publish("arduino"+Arduino+"/button"+Pin+"/status", "L", 0, False)
			mqttc.publish("arduino"+Arduino+"/button"+Pin+"/status", "H", 0, False)
			printLog(debug,"Toggle() "+"[" + str(datetime.datetime.now()) + "] arduino"+Arduino+"/button"+Pin+"/Triggerd")

def scheduleDay(List,Day):
	for timer in List:
		naam,Time,arduino,pin = timer.split("|")
		args = (naam , arduino , pin)
		kw = {
			"func": Toggle,
			"parm": args,
			}
		
		if Day == 0:
			schedule.every().day.at(Time).do(run_threaded, **kw)
			printLog(info,"Scheduled every day: " + naam + " on : " + Time)
		elif Day == 1:
			schedule.every().monday.at(Time).do(run_threaded, **kw)
			printLog(info,"Scheduled every Monday: " + naam + " on : " + Time)
		elif Day == 2:
			schedule.every().tuesday.at(Time).do(run_threaded, **kw)
			printLog(info,"Scheduled every Tuesday: " + naam + " on : " + Time)
		elif Day == 3:
			schedule.every().wednesday.at(Time).do(run_threaded, **kw)
			printLog(info,"Scheduled every Wednesday: " + naam + " on : " + Time)
		elif Day == 4:
			schedule.every().thursday.at(Time).do(run_threaded, **kw)
			printLog(info,"Scheduled every Thursday: " + naam + " on : " + Time)		
		elif Day == 5:
			schedule.every().friday.at(Time).do(run_threaded, **kw)
			printLog(info,"Scheduled every Friday: " + naam + " on : " + Time)
		elif Day == 6:
			schedule.every().saturday.at(Time).do(run_threaded, **kw)
			printLog(info,"Scheduled every Saturday: " + naam + " on : " + Time)
		elif Day == 7:
			schedule.every().sunday.at(Time).do(run_threaded, **kw)
			printLog(info,"Scheduled every Sunday: " + naam + " on : " + Time)

check = False
#Schedule Days
scheduleDay(EverydayList,0)
scheduleDay(MondayList,1)
scheduleDay(TuesdayList,2)
scheduleDay(WednesdayList,3)
scheduleDay(ThursdayList,4)
scheduleDay(FridayList,5)
scheduleDay(SaturdayList,6)
scheduleDay(SundayList,7)

	
#Needed for recalculating sunrise & sunset
schedule.every().day.at("00:00").do(restart)
printLog(info,"Scheduled every day: RESET on : 00:00")


while True:
        schedule.run_pending()
        mqttc.loop()
