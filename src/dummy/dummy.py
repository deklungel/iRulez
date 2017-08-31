import logging
import src.irulez.db
import src.lib.paho.mqtt.client as mqtt

logger = logging.getLogger('dummy')
logger.info('Dummy starting')

# Get database, dummy for now
db = src.irulez.db.get_dummy_db()

# Initialize relay states
relays = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


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
    global relays
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")
    # convert the incoming payload in hex to a binary with leading 0
    action = bin(int(msg.payload, 16))[2:].zfill(32)
    on = list(action[:16])
    off = list(action[16:])
    # Loop 16 times and update the relays array.
    for x in range(0, 15):
        if on[x] == 1:
            relays[x] = 1
        if off[x] == 1:
            relays[x] = 0
    # Make a string from the array
    status = ''.join(relays)
    # create a hex from the string
    status = hex(int(status))
    # Publish the status
    client.publish("iRulezIO16_1/status", str(status))

# Create client
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect
mqttConfig = db.get_mqtt_config()

client.username_pw_set(mqttConfig.username, mqttConfig.password)
client.connect(mqttConfig.address, mqttConfig.port, 60)

# Blocking class that loops forever
# Also handles reconnecting
client.loop_forever()
