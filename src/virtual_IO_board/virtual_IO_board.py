import src.irulez.log as log
import src.irulez.db
import src.irulez.constants as constants
import src.irulez.util as util
import lib.paho.mqtt.client as mqtt
from src.irulez import configuration

logger = log.get_logger('virtual_IO_board')

#TODO: update code to get_virtual_IO not dummy DB
# Get database, dummy for now
db = src.irulez.db.get_dummy_db()

def on_connect(client, userdata, flags, rc):
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))
    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    logger.debug("Subscribing to " + str(constants.arduinoTopic) + "/" + constants.virtual_IO_board_name + "/" + constants.actionTopic)
    client.subscribe(constants.arduinoTopic  + "/" + constants.virtual_IO_board_name + "/" + constants.actionTopic)
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


    logger.debug(f"Publishing new status of arduino '{constants.virtual_IO_board_name}: {msg.payload}'")
    client.publish(constants.arduinoTopic + '/' + constants.virtual_IO_board_name + '/status', str(msg.payload.decode('ascii')),0,True)




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
