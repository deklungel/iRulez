import src.button.factory as factory
import lib.paho.mqtt.client as mqtt
import src.button._db
import src.button.mqtt_sender as mqtt_sender
import src.button.processors as button_processor
import src.irulez.configuration as configuration
import src.irulez.constants as constants
import src.irulez.log as log
import src.irulez.util as util
import src.output_status.ServiceClient as ServiceClient
import src.button._action_executor as action_executor

logger = log.get_logger('button')

# Get database, dummy for now
logger.debug('Getting database')
db = src.button._db.get_maria_db()
factory = factory.ArduinoConfigFactory(db)

# Connect
config = configuration.Configuration()
mqttConfig = config.get_mqtt_config()
serviceConfig = config.get_service_client_config()

# Get arduinos from database and store them in a dictionary
# Key is the name of the arduino
logger.debug('Creating arduinos')
arduinos = {}
for arduino in factory.create_arduino_config().arduinos:
    arduinos[arduino.name] = arduino

# Create client
client = mqtt.Client()
sender = mqtt_sender.MqttSender(client, arduinos)
StatusService = ServiceClient.StatusServiceClient(serviceConfig['url'], serviceConfig['port'])
executor = action_executor.ActionExecutor(sender, StatusService)
action_processor = button_processor.ButtonActionProcessor(executor, arduinos, sender)


def on_connect(connected_client, _, __, rc) -> None:
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))

    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    logger.debug("Subscribing to " + str(constants.iRulezTopic) + "/+/" + constants.buttonTopic)
    connected_client.subscribe(constants.iRulezTopic + "/+/" + constants.buttonTopic)
    logger.debug("Subscribing to " + str(constants.iRulezTopic) + "/" + constants.buttonTimerFiredTopic)
    connected_client.subscribe(constants.iRulezTopic + "/" + constants.buttonTimerFiredTopic)
    logger.debug("Subscribing to " + str(constants.iRulezTopic) + "/" + constants.buttonMulticlickFiredTopic)
    connected_client.subscribe(constants.iRulezTopic + "/" + constants.buttonMulticlickFiredTopic)


def on_subscribe(_, __, mid, granted_qos) -> None:
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(_, __, msg) -> None:
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")

    # Get the name of the arduino from the topic
    name = util.get_arduino_name_from_topic(msg.topic)

    # Check if the topic is a longdown fired topic
    if util.is_arduino_button_fired_topic(msg.topic):
        logger.debug("Button fired received.")
        action_processor.button_timer_fired(msg.payload)
        return

    # Check if the topic is a multiclick fired topic
    if util.is_arduino_multiclick_fired_topic(msg.topic):
        logger.debug("Button Multiclick received.")
        action_processor.button_multiclick_fired(msg.payload)
        return

    # Check if the topic is a relay or button update.
    if util.is_arduino_button_topic(msg.topic):
        logger.debug(f"Button change received.")
        action_processor.process_button_message(name, msg.payload)
        return

    logger.warning(f"Topic '{msg.topic}' is of no interest to us. Are we subscribed to too much?")


# Set callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe


client.username_pw_set(mqttConfig['username'], mqttConfig['password'])
client.connect(mqttConfig['ip'], int(mqttConfig['port']), 60)


logger.info("Starting loop forever")
# Blocking class that loops forever
# Also handles reconnecting
client.loop_forever()
