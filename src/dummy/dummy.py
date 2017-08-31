import logging
import src.irulez.db
import paho.mqtt.client as mqtt

logger = logging.getLogger('dummy')
logger.info('Dummy starting')
db = src.irulez.db.get_dummy_db()

relais = bin(0).zfill(32)

def on_connect(client, userdata, flags, rc):
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))

    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino relay actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    client.subscribe("iRulezIO16_+/action")

    # Subscribe to dimmer values


def on_message(client, userdata, msg):
    global relais
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")
    # convert the incomming payload in hex to a biniry with leading 0
    action = bin(int(msg.payload, 16))[2:].zfill(32)
    ON = action[:16]
    OFF = action[16:]


    client.publish("iRulezIO16_1/status",)

# Create client
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect
mqttConfig = db.get_mqtt_config()

client.username_pw_set(mqttConfig.username,mqttConfig.password)
client.connect(mqttConfig.address, mqttConfig.port, 60)

# Blocking class that loops forever
# Also handles reconnecting
client.loop_forever()
