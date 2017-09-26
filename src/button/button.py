import logging
import src.irulez.db
import src.irulez.constants as constants
import lib.paho.mqtt.client as mqtt
import src.irulez.util as util
import src.irulez.domain as domain

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
    logger.debug("Subscribing to " + str(constants.arduinoTopic) + "/+/" + constants.buttonTopic)
    client.subscribe(constants.arduinoTopic + "/+/" + constants.buttonTopic)
    logger.debug("Subscribing to " + str(constants.arduinoTopic) + "/+/" + constants.statusTopic)
    client.subscribe(constants.arduinoTopic + "/+/" + constants.statusTopic)


def on_subscribe(mqttc, obj, mid, granted_qos):
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def update_arduino_output_pins(name, payload):
    global arduinos
    arduino = arduinos.get(name, None)
    if arduino is None:
        # Unknown arduino
        logger.info(f"Could not find arduino with name '{name}'.")
        return
    arduino.set_relay_status(payload)


def send_Relative_Update(registersON, registersOFF):
    pass


def process_Button(arduino, pin , value):
    actions = arduino.button_pins[pin].get__button_pin_actions()
    registersON = {}
    registersOFF = {}
    for action in actions:
        if(action.action_type.get_action_trigger_type() == domain.ActionTriggerType.IMMEDIATELY and value == True):
            logger.info(f"Process action Immediatly")
            if(action.action_type == domain.ActionType.ON):
                pins = action.relay_pins
                for pin in pins:
                    registersON.setdefault(arduino.name, []).append(pin.number)
            elif(action.action_type == domain.ActionType.OFF):
                pins = action.relay_pins
                for pin in pins:
                    registersOFF.setdefault(arduino.name, []).append(pin.number)
        elif(action.action_type.get_action_trigger_type() == domain.ActionTriggerType.AFTER_RELEASE and value == False):
            logger.info(f"Process action After Release")
    
    send_Relative_Update(registersON,registersOFF)


def process_Button_Message(name, payload):
    global arduinos
    arduino = arduinos.get(name, None)
    if arduino is None:
        # Unknown arduino
        logger.info(f"Could not find arduino with name '{name}'.")
        return
    changed_pins = arduino.get_changed_pins(payload)
    for pin, value in changed_pins.items():
        process_Button(arduino, pin,value)





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

    # Check if the toppic is a relay or button update.
    if (util.is_arduino_status_topic(msg.topic)):
        logger.debug(f"Update the relay status")
        update_arduino_output_pins(name, msg.payload)
        return

    elif (util.is_arduino_button_topic(msg.topic)):
        logger.debug(f"Button change receiveid.")
        process_Button_Message(name, msg.payload)
        return

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
