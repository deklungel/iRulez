#!/usr/bin/env python
#Version 1.9
import sys
sys.path.append('/var/www/html/modules/libraries')
import time
import pprint
import telepot
import mysql.connector
import datetime
import iRulez_logging as logger
import paho.mqtt.client as mqtt
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from inspect import currentframe


file = open('/var/www/html/config.php', 'r')

debug = "DEBUG"
info = "INFO"
alert = "ALERT"

logger.printLog(info,'**** Telgram Started ****', str(logger.get_linenumber()))

for line in file:
	if "db_name" in line: MySQL_database = line.split('"')[3]
	elif "db_user" in line: MySQL_username = line.split('"')[3]
	elif "db_password" in line: MySQL_password = line.split('"')[3]


	
try:	
	cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
	cursor = cnx.cursor()
	query = ("SELECT Setting,value FROM Settings")
	logger.printLog(debug,query,str(logger.get_linenumber()))
	cursor.execute(query)	
	for (Setting, value) in cursor:
		if Setting == "MQTT_ip_address":
			MQTT_ip_address = value
		elif Setting == "MQTT_port_python":
			MQTT_port = int(value)
		elif Setting == "BotID":
			BotIDTmp = value
		elif Setting == "TokenBOT":
			BotToken = value
		elif Setting == "NotificationSnooze":
			NotificationSnooze = value
		elif Setting == "TimeBetweenNotification":
			TimeBetweenNotification = value
		elif Setting == "Notification Method":
			NotificationMethod = value
			
	if BotToken == "":
		raise Exception('NO BotToken provided')
except Exception as e:
	logger.printLog(alert,e,str(logger.get_linenumber()))
	raise
finally:	
	cursor.close()
	cnx.close()	

BotIDS = BotIDTmp.split('|')


AllLow = []
AllLowN = []


def handle(msg):

	chat_id = msg['chat']['id']
	command = msg['text']
	
	logger.printLog(debug,'Got command: %s' % command, str(logger.get_linenumber()))
	logger.printLog(debug,'Got chatID from : %s' % chat_id, str(logger.get_linenumber()))
	
	if str(chat_id) in BotIDS:
		if command == '/status':
			try:
				cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
				cursor = cnx.cursor()
				query = ("SELECT naam, arduino, pin FROM Core_Arduino_Outputs WHERE Status = 'ON' AND telegram = '1'")
				logger.printLog(debug,str(query), str(logger.get_linenumber()))
				cursor.execute(query)
				NotificationList = []
				for (naam,arduino,pin) in cursor:
					NotificationList.append([naam,arduino,pin])
			except Exception as e:
				logger.printLog(alert,e,str(logger.get_linenumber()))
				raise
			finally:	
				cursor.close()
				cnx.close()	

			KeyBoardArray = []
			if len(NotificationList) > 0:
				Message = "Following lights are on"
			else:
				Message = "No lights are on!"
			global AllLow
			AllLow = []
			for Notication in NotificationList:
				text = str(Notication[0])
				callback = NotificationMethod+'|Low|;'+str(Notication[0])+';'+str(Notication[1])+';'+str(Notication[2])
				KeyBoardArray.append( [InlineKeyboardButton(text=str(text), callback_data=str(callback))],)
				AllLow.append([Notication[1],Notication[2]])
			if len(NotificationList) > 1:
				text = "* Alles uit *"
				callback = NotificationMethod+'|Low|AllLow'
				KeyBoardArray.append( [InlineKeyboardButton(text=str(text), callback_data=str(callback))],)
			

			markup = InlineKeyboardMarkup(inline_keyboard=KeyBoardArray)
			

			logger.printLog(debug,"status has been send to "+ str(chat_id), str(logger.get_linenumber()))	 
			bot.sendMessage(chat_id,  Message, reply_markup=markup)
		
	elif command == '/enroll':
			hide_keyboard = {'hide_keyboard': True}
			text = 'Give this ID to you iRulez Administrator: '+str(chat_id)
			logger.printLog(debug,"Enrollment has been send to "+ str(chat_id), str(logger.get_linenumber()))	 
			bot.sendMessage(chat_id, text , reply_markup=hide_keyboard)
		
		# elif command == '/time':
			# show_keyboard = {'keyboard': [['Yes','No']]}
			# hide_keyboard = {'hide_keyboard': True}
			# bot.sendMessage(chat_id, 'This is a custom keyboard', reply_markup=hide_keyboard)

def on_callback_query(msg):
	query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
	logger.printLog(debug,'Callback query:'+ str(query_id) +' '+ str(from_id) +' '+ str(data), str(logger.get_linenumber()))
	actionsArr = data.split('|')
	global AllLowN
	global AllLow
	relais = actionsArr[2].split(';')
	if actionsArr[1] == "Low":
			if relais[0] == "AllLow":
				tmpText = "All Lights are out"
				for relais in AllLow:
					topic = "arduino"+str(relais[0])+"/relais"+str(relais[1])+"/action"
					payload ="L"
					logger.printLog(debug,"Publish: " + topic +":"+ payload , str(logger.get_linenumber()) )
					mqttc.publish(topic,payload, 0, False)	
			elif relais[0] == "AllLowN":
				tmpText = "All Lights are out"
				global AllLowN 
				for relais in AllLowN:
					topic = "arduino"+str(relais[1])+"/relais"+str(relais[2])+"/action"
					payload ="L"
					logger.printLog(debug,"Publish: " + topic +":"+ payload , str(logger.get_linenumber()) )
					mqttc.publish(topic,payload, 0, False)	
			else:
				tmpText = relais[1]+" out"
				topic = "arduino"+str(relais[2])+"/relais"+str(relais[3])+"/action"
				payload ="L"
				logger.printLog(debug,"Publish: " + topic +":"+ payload , str(logger.get_linenumber()) )
				mqttc.publish(topic,payload, 0, False)	
		
		
	elif actionsArr[1] == "Ignore":
		try:
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			for relais in AllLowN:
				query = ("UPDATE Core_Arduino_Outputs SET notification_dismiss = 1 WHERE id="+str(relais[0]))
				logger.printLog(debug,query, str(logger.get_linenumber()))
				cursor.execute(query)
				cnx.commit()
		except Exception as e:
			logger.printLog(alert,e,str(logger.get_linenumber())) 
			raise
		finally:	
			cursor.close()
			cnx.close()	
		tmpText = "Notification ignored"
	elif actionsArr[1] == "Snooze":
		Time = datetime.datetime.now() + datetime.timedelta(seconds=int(NotificationSnooze)*60)
		try:
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			for relais in AllLowN:
				query = ("UPDATE Core_Arduino_Outputs SET notification_snooze = '"+str(Time)+"' WHERE id="+str(relais[0]))
				logger.printLog(debug,query, str(logger.get_linenumber()))
				cursor.execute(query)
				cnx.commit()
		except Exception as e:
			logger.printLog(alert,e,str(logger.get_linenumber())) 
			raise
		finally:	
			cursor.close()
			cnx.close()	
		tmpText = "Notifications Snoozed for "+str(NotificationSnooze)+"min"
		
	if actionsArr[0] == 'notification':
		logger.printLog(debug,"Notification has been send to "+ str(query_id), str(logger.get_linenumber()))
		bot.answerCallbackQuery(query_id, text=tmpText)
	elif actionsArr[0] == 'alert':
		logger.printLog(debug,"Alert has been send to "+ str(query_id), str(logger.get_linenumber()))
		bot.answerCallbackQuery(query_id, text=tmpText, show_alert=True)
 
def on_connect(mqttc, obj, rc):
	logger.printLog(debug,"rc: "+str(rc) , str(logger.get_linenumber()))

def on_message(mqttc, obj, msg):	
	hide_keyboard = {'hide_keyboard': True}
	for BotID in BotIDS:
			logger.printLog(debug,"Notification message has been send to "+BotID, str(logger.get_linenumber()))	 
			bot.sendMessage(int(BotID), str(msg.payload) , reply_markup=hide_keyboard)
	
def on_publish(mqttc, obj, mid):
	logger.printLog(debug,"Publish: "+str(mid), str(logger.get_linenumber()))
	
def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.printLog(debug,"Subscribed: "+str(mid)+" "+str(granted_qos) , str(logger.get_linenumber()))

def on_log(mqttc, obj, level, string):
    logger.printLog(debug,string , str(logger.get_linenumber()))	

def on_disconnect(client, userdata, rc):
	logger.printLog(info, "on_disconnect!", str(logger.get_linenumber()))
	exit()	
 
def checkRelay():
	try:
		cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
		cursor = cnx.cursor()
		query = ("SELECT id, naam, status_time, notification, arduino, pin, notification_snooze FROM Core_Arduino_Outputs WHERE notification IS NOT NULL AND notification <> '' AND notification_dismiss = 0 AND status = 'ON' ")
		
		logger.printLog(debug,str(query), str(logger.get_linenumber()))
		cursor.execute(query)
		NotificationList = []
		for (id, naam, Time_on, notification,arduino,pin,snooze) in cursor:
			logger.printLog(debug,'Found Record: %s' % naam, str(logger.get_linenumber()))
			Time =  datetime.datetime.now()
			time_delta = (Time - Time_on).total_seconds()
			if (int(time_delta) > int(notification)):
				if snooze is None:
					logger.printLog(debug,'Add : %s to notification list NOT SNOOZED' % naam, str(logger.get_linenumber()))
					NotificationList.append([id,naam,arduino,pin])
				else:
					if snooze < Time :
						logger.printLog(debug,'Add : %s to notification list SNOOZED' % naam, str(logger.get_linenumber()))
						NotificationList.append([id,naam,arduino,pin])
	except Exception as e:
			logger.printLog(alert,e,str(logger.get_linenumber()))
			raise
	finally:	
		cursor.close()
		cnx.close()	
	
	if len(NotificationList) >0:
		KeyBoardArray = []
		Message = "Following lights are on"
		global AllLowN
		AllLowN = []
		for Notication in NotificationList:
			text = str(Notication[1])
			callback = NotificationMethod+'|Low|'+str(Notication[0])+';'+str(Notication[1])+';'+str(Notication[2])+';'+str(Notication[3])
			KeyBoardArray.append( [InlineKeyboardButton(text=str(text), callback_data=str(callback))],)
			AllLowN.append([Notication[0],Notication[2],Notication[3]])
		if len(NotificationList) > 1:
			text = "* Alles uit *"
			callback = NotificationMethod+'|Low|AllLowN'
			KeyBoardArray.append( [InlineKeyboardButton(text=str(text), callback_data=str(callback))],)
		text = "* Ignore *"
		callback = NotificationMethod+'|Ignore|'
		KeyBoardArray.append( [InlineKeyboardButton(text=str(text), callback_data=str(callback))],)
		text = "* Snooze "+str(NotificationSnooze)+"min *"
		callback = NotificationMethod+'|Snooze|'
		KeyBoardArray.append( [InlineKeyboardButton(text=str(text), callback_data=str(callback))],)
		
		markup = InlineKeyboardMarkup(inline_keyboard=KeyBoardArray)
		for BotID in BotIDS:
			logger.printLog(debug,"Notification message has been send to "+BotID, str(logger.get_linenumber()))	 
			bot.sendMessage(int(BotID),  Message, reply_markup=markup)
		
		Time = datetime.datetime.now() + datetime.timedelta(seconds=int(TimeBetweenNotification)*60)
		try:
			cnx = mysql.connector.connect(user=MySQL_username,password=MySQL_password,database=MySQL_database)
			cursor = cnx.cursor()
			for relais in AllLowN:
				query = ("UPDATE Core_Arduino_Outputs SET notification_snooze = '"+str(Time)+"' WHERE id="+str(relais[0]))
				logger.printLog(debug,query, str(logger.get_linenumber()))
				cursor.execute(query)
				cnx.commit()
		except Exception as e:
			logger.printLog(alert,e,str(logger.get_linenumber()))
			raise
		finally:	
			cursor.close()
			cnx.close()	
		#tmpText = "Notifications Snoozed for "+str(NotificationSnooze)+"min"


bot = telepot.Bot(BotToken)
bot.message_loop({'chat': handle,'callback_query': on_callback_query})
logger.printLog(info,"Listening ...",str(logger.get_linenumber()))
# Keep the program running.
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
mqttc.subscribe("Telegram/Message", 0)

counter = int(time.time())
while True:
	mqttc.loop()
	if(counter + 10 <= int(time.time())):
		checkRelay()
		counter = int(time.time()) 