import src.button._factory as factory

import paho.mqtt.client as mqtt
import src.button._db
import src.irulez.configuration as configuration
import src.irulez.constants as constants
import src.irulez.log as log
import src.irulez.util as util

logger = log.get_logger('dummy')

# Get database, dummy for now
logger.debug('Getting database')
db = src.button._db.get_maria_db()
factory = factory.ArduinoConfigFactory(db)

# Get arduinos from database and store them in a dictionary
# Key is the name of the arduino
logger.debug('Creating arduinos')
arduinos = {}
for ard in factory.create_arduino_config().arduinos:
    arduinos[ard.name] = ard


def on_connect(connected_client, _, __, rc) -> None:
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))
    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    logger.debug("Subscribing to " + str(constants.iRulezTopic) + "/+/" + constants.actionTopic)
    connected_client.subscribe(constants.iRulezTopic + "/+/" + constants.actionTopic)

    logger.debug("Subscribing to " + str(constants.iRulezTopic) + "/" + '+' + "/" +
                 constants.dimAction + "/+")
    connected_client.subscribe(constants.iRulezTopic + "/" + '+' + "/" +
                               constants.dimAction + "/+")


def on_subscribe(_, __, mid, granted_qos) -> None:
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(_, __, msg) -> None:
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")
    global arduinos

    if util.is_arduino_action_topic(msg.topic):
        handle_arduino_action(msg)
    elif util.is_arduino_dim_action_topic(msg.topic):
        handle_arduino_dim_action(msg)
    else:
        logger.warning(f"Topic '{msg.topic}' is of no interest to us. Are we subscribed to too much?")


def handle_arduino_dim_action(msg) -> None:
    # Get the name of the arduino from the topic
    name = util.get_arduino_name_from_topic(msg.topic)

    # .get(key, None) gets the element with key from a dictionary or None if it doesn't exist
    arduino = arduinos.get(name, None)
    if arduino is None:
        # Unknown arduino
        logger.info(f"Could not find arduino with name '{name}'.")
        return

    pin_number = msg.topic[len(constants.iRulezTopic + '/' + name + '/' + constants.dimAction + '/'):]
    value = int(msg.payload)
    logger.debug(f"Got dim action for arduino '{name}' and pin '{pin_number}' with value '{value}'")

    pin = arduino.output_pins.get(pin_number, None)
    if pin is None:
        logger.warning(f"Arduino '{name}' has no pin with number '{pin_number}'")

    logger.debug(f"Publishing new dimmer status of arduino '{name}', pin '{pin_number}': '{value}'")
    client.publish(constants.iRulezTopic + '/' + name + '/' + pin_number + '/' + constants.dimmerStatusTopic,
                   value,
                   0,
                   False)


def handle_arduino_action(msg) -> None:
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
    client.publish(constants.iRulezTopic + '/' + name + '/status', status, 0, False)


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
