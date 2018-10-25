import src.irulez.log as log
import lib.paho.mqtt.client as mqtt
import src.irulez.constants as constants
import src.output_status.db as db
import src.irulez.util as util
import src.irulez.topic_factory as topic_factory
import src.output_status.processors as service_processor
import src.irulez.configuration as configuration
import src.output_status.factory as factory
import src.output_status.ServiceServer as ServiceServer

logger = log.get_logger('Service')

# Get database, dummy for now
logger.debug('Getting database')
db = db.get_maria_db()
factory = factory.ArduinoConfigFactory(db)

# Get arduinos from database and store them in a dictionary
# Key is the name of the arduino
logger.debug('Creating arduinos')
arduinos = {}
for arduino in factory.create_arduino_config().arduinos:
    arduinos[arduino.name] = arduino

dimmer_light_values = {}

# Create client
client = mqtt.Client()
update_processor = service_processor.ServiceProcessor(arduinos, dimmer_light_values)


def on_connect(connected_client, _, __, rc) -> None:
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))

    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    logger.debug("Subscribing to " + str(constants.iRulezTopic) + "/+/" + constants.statusTopic)
    connected_client.subscribe(constants.iRulezTopic + "/+/" + constants.statusTopic)
    connected_client.subscribe(constants.iRulezTopic + "/+/+/" + constants.dimmerStatusTopic)
    connected_client.subscribe(topic_factory.create_last_light_value_update_topic())


def on_subscribe(_, __, mid, granted_qos) -> None:
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(_, __, msg) -> None:
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")

    # Get the name of the arduino from the topic
    name = util.get_arduino_name_from_topic(msg.topic)

    # Process message
    if util.is_arduino_status_topic(msg.topic):
        logger.debug(f"Update the relay status of a normal arduino")
        update_processor.update_arduino_output_pins(name, msg.payload)
    elif util.is_arduino_dimmer_status_topic(msg.topic):
        dimmer_pin = util.get_arduino_dimmer_pin_from_topic(msg.topic, name)
        logger.debug(f"Update the relay status of a dimmer")
        update_processor.update_arduino_dimmer_pins(name, dimmer_pin, msg.payload)
    elif util.is_irulez_last_light_value_event_topic(msg.topic):
        logger.debug(f"Last_light_value received")
        update_processor.update_last_light_value(msg.payload)
    else:
        logger.warning(f"Topic '{msg.topic}' is of no interest to us. Are we subscribed to too much?")


# Set callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Connect
config = configuration.Configuration()
mqttConfig = config.get_mqtt_config()
serviceConfig = config.get_service_server_config()

client.username_pw_set(mqttConfig['username'], mqttConfig['password'])
client.connect(mqttConfig['ip'], int(mqttConfig['port']), 60)

StatusServiceServer = ServiceServer.OutputServiceServer(arduinos,
                                                        dimmer_light_values,
                                                        serviceConfig['url'],
                                                        int(serviceConfig['port']))
StatusServiceServer.connect()

logger.info("Starting loop forever")
# Blocking class that loops forever
# Also handles reconnecting
client.loop_forever()
