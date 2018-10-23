import src.irulez.log as log
import src.irulez.constants as constants
import src.irulez.util as util
import lib.paho.mqtt.client as mqtt
import src.irulez.configuration as configuration
import src.relative_convertor.processors as relative_processor
import src.relative_convertor.mqtt_sender as mqtt_sender
import src.output_status.ServiceClient as ServiceClient


logger = log.get_logger('absolute_update')

# Get config
config = configuration.Configuration()
mqttConfig = config.get_mqtt_config()
serviceConfig = config.get_service_client_config()

# Create client
client = mqtt.Client()
StatusService = ServiceClient.StatusServiceClient(serviceConfig['url'], serviceConfig['port'])
sender = mqtt_sender.MqttSender(client, StatusService)
relative_action_processor = relative_processor.RelativeActionProcessor(sender)


def on_connect(connected_client, _, __, rc) -> None:
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))
    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    logger.debug("Subscribing to " + str(constants.iRulezTopic) + "/" + constants.actionTopic + "/" +
                 constants.relativeTopic)
    connected_client.subscribe(constants.iRulezTopic + "/" + constants.actionTopic + "/" + constants.relativeTopic)


def on_subscribe(_, __, mid, granted_qos) -> None:
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(_, __, msg) -> None:
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")

    # Find arduino name of topic
    if not util.is_arduino_relative_action_topic(msg.topic):
        logger.warning(f"Topic '{msg.topic}' is of no interest to us. Are we subscribed to too much?")
        # Unknown topic
        return

    logger.debug(f"Convert relative to absolute ")
    relative_action_processor.process_relative_action_message(msg.payload.decode("utf-8"))


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
