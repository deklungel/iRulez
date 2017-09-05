import lib.paho.mqtt.publish as publish
import src.irulez.db
import src.irulez.constants as constants
import src.irulez.util as util

# Get database, dummy for now
db = src.irulez.db.get_dummy_db()

# Connect
mqttConfig = db.get_mqtt_config()


arduino = input("Arduino name? <dummy> " or "dummy")
pin = input("Pin 0 <-> 15 " or "5")
state = input("H | L " or "H")

arduino = "dummy"


pin_states = [0]*32

if(state == 'H'):
    pin_states[int(pin)] = 1
else:
    pin_states[16 + int(pin)] = 1




payload = util.convert_array_to_hex(pin_states)

print(constants.arduinoTopic + "/" + arduino + "/" + constants.actionTopic + "/hexnumber/" +payload)

publish.single(constants.arduinoTopic + "/" + arduino + "/" +constants.actionTopic + "/hexnumber",payload,auth={'username': mqttConfig.username, 'password': mqttConfig.password}, hostname=mqttConfig.address, port=mqttConfig.port,retain=False)