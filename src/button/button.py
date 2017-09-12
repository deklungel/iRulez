import logging
import src.irulez.db
import src.irulez.constants as constants
import src.irulez.util as util
import lib.paho.mqtt.client as mqtt

logger = logging.getLogger('dummy')
logger.info('Dummy starting')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# Get database, dummy for now
db = src.irulez.db.get_dummy_db()

# Get arduinos from database and store them in a dictionary
# Key is the name of the arduino
arduinos = {}
for arduino in db.get_arduino_config().arduinos:
    arduinos[arduino.name] = arduino

def on_connect(client, userdata, flags, rc):
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))
    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    logger.debug("Subscribing to " + str(constants.arduinoTopic) + "/+/" + constants.buttonTopic )
    client.subscribe(constants.arduinoTopic + "/+/" + constants.buttonTopic)

def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")


# Create client
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Connect
mqttConfig = db.get_mqtt_config()

client.username_pw_set(mqttConfig.username, mqttConfig.password)
client.connect(mqttConfig.address, mqttConfig.port, 60)

logger.info("Starting loop forever")
# Blocking class that loops forever
# Also handles reconnecting
client.loop_forever()
