import lib.paho.mqtt.publish as publish
import src.irulez.db
import src.irulez.constants as constants
import src.irulez.util as util

# Get database, dummy for now
db = src.irulez.db.get_dummy_db()

# Connect
mqttConfig = db.get_mqtt_config()


arduino = input("Arduino name? <DEMO> " or "DEMO")
pin = input("Pin 0 <-> 15 " or "5")

pin_states = [0]*16

list = pin.split('|');
for relay in list:
    pin_states[int(relay)] = 1


payload = util.convert_array_to_hex(pin_states)

print(constants.arduinoTopic + "/" + arduino + "/" + constants.actionTopic + "/" + payload)

publish.single(constants.arduinoTopic + "/" + arduino + "/" + constants.actionTopic , payload,
               auth={'username': mqttConfig.username, 'password': mqttConfig.password}, hostname=mqttConfig.address,
               port=mqttConfig.port, retain=False)
