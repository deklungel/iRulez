import src.irulez.factory as factory

import lib.paho.mqtt.client as mqtt
import src.button.db
import src.irulez.configuration as configuration
import src.irulez.constants as constants
import src.irulez.log as log
import src.irulez.util as util

logger = log.get_logger('dummy')

# Get database, dummy for now
logger.debug('Getting database')
db = src.button.db.get_maria_db()
factory = factory.ArduinoConfigFactory(db)

# Get arduinos from database and store them in a dictionary
# Key is the name of the arduino
logger.debug('Creating arduinos')
arduinos = {}
for arduino in factory.create_arduino_config().arduinos:
    arduinos[arduino.name] = arduino


def on_connect(client, userdata, flags, rc):
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))
    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    logger.debug("Subscribing to " + str(constants.arduinoTopic) + "/+/" + constants.actionTopic)
    client.subscribe(constants.arduinoTopic + "/+/" + constants.actionTopic)
    # TODO: Subscribe to dimmer values


def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")
    global arduinos

    # Find arduino name of topic
    if not (util.is_arduino_action_topic(msg.topic)):
        logger.warning(f"Topic '{msg.topic}' is of no interest to us. Are we subscribed to too much?")
        # Unknown topic
        return

    # Get the name of the arduino from the topic
    name = util.get_arduino_name_from_topic(msg.topic)

    # .get(key, None) gets the element with key from a dictionary or None if it doesn't exist
    arduino = arduinos.get(name, None)
    if arduino is None:
        # Unknown arduino
        logger.info(f"Could not find arduino with name '{name}'.")
        return

    # Convert the incoming payload in hex to a binary with leading 0
    output_pin_actions = util.convert_hex_to_array(msg.payload, arduino.number_of_output_pins)
    # Loop over all relay_pins of the arduino and update if needed
    for pin in arduino.output_pins.values():
        if pin.number < 0 or pin.number > (arduino.number_of_output_pins - 1):
            logger.warning(f"Arduino '{name}' has a pin with number '{pin.number}'.")
            # Continue hops to the next iteration of the for-loop
            continue

        if output_pin_actions[pin.number] == '1':
            pin.state = True
        else:
            pin.state = False

    # Publish new status
    status = arduino.get_output_pin_status()
    logger.debug(f"Publishing new status of arduino '{name}': '{status}'")
    client.publish(constants.arduinoTopic + '/' + name + '/status', status, True)


# Create client
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Connect
config = configuration.Configuration()
mqttConfig = config.get_mqtt_config()

client.username_pw_set(mqttConfig['username'], mqttConfig['password'])
client.connect(mqttConfig['ip'], int(mqttConfig['port']), 60)

logger.info("Starting loop forever")
# Blocking class that loops forever
# Also handles reconnecting
client.loop_forever()
