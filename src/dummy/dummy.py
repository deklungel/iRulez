import logging
import src.irulez.db
import src.irulez.constants as constants
import src.irulez.util as util
import paho.mqtt.client as mqtt

logger = logging.getLogger('dummy')
logger.info('Dummy starting')

# Get database, dummy for now
db = src.irulez.db.get_dummy_db()

# Get arduinos from database and store them in a dictionary
# Key is the name of the arduino
arduinos = {}
for arduino in db.get_arduino_config.arduinos:
    arduinos[arduino.name] = arduino


def on_connect(client, userdata, flags, rc):
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))

    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    client.subscribe(constants.arduinoTopic + "+/action/hexnumber")

    # TODO: Subscribe to dimmer values


def on_message(client, userdata, msg):
    global arduinos
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")

    # Find arduino name of topic
    if not(util.is_arduino_action_topic(msg.topic)):
        logger.warning(f"Topic '{msg.topic}' is of no interest to us. Are we subscribed to too much?")
        # Unknown topic
        return

    name = util.get_arduino_name_from_topic(msg.topic)
    arduino = arduinos.get(name, None)
    if arduino is None:
        # Unknown arduino
        logger.info(f"Could not find arduino with name '{name}'.")
        return

    # Convert the incoming payload in hex to a binary with leading 0
    action = bin(int(msg.payload, 16))[2:].zfill(32)
    on = list(action[:16])
    off = list(action[16:])

    for pin in arduino.pins.values():
        if pin.number < 0 or pin.number > 15:
            logger.warning(f"Arduino '{name}' has a pin with number '{pin.number}'.")
            continue
        if on[pin.number] == 1:
            pin.state = True
        if off[pin.number] == 1:
            pin.state = False

    status = arduino.get_relay_status()
    client.publish(constants.arduinoTopic + name + '/status', str(status))


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
