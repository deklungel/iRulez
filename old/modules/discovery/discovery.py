#!/usr/bin/env python

import sys
sys.path.append('/var/www/html/modules/libraries')
import avahi
import dbus
from time import sleep
import mysql.connector


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
cursor.close()
cnx.close()	


class ServiceAnnouncer:
    def __init__(self, name, service, port, txt):
        bus = dbus.SystemBus()
        server = dbus.Interface(bus.get_object(avahi.DBUS_NAME, avahi.DBUS_PATH_SERVER), avahi.DBUS_INTERFACE_SERVER)
        group = dbus.Interface(bus.get_object(avahi.DBUS_NAME, server.EntryGroupNew()),
                               avahi.DBUS_INTERFACE_ENTRY_GROUP)

        self._service_name = name
        index = 1
        while True:
            try:
                group.AddService(avahi.IF_UNSPEC, avahi.PROTO_INET, 0, self._service_name, service, '', '', port, avahi.string_array_to_txt_array(txt))
            except dbus.DBusException: # name collision -> rename
                index += 1
                self._service_name = '%s #%s' % (name, str(index))
            else:
                break

        group.Commit()

    def get_service_name(self):
        return self._service_name



if __name__ == '__main__':
    announcer = ServiceAnnouncer(MQTT_ip_address, '_irulez._tcp.', 80,'')
    print announcer.get_service_name()

    sleep(10000)
