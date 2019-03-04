import src.irulez.log as log
import src.irulez.constants as constants
import src.irulez.util as util
import paho.mqtt.client as mqtt
import src.irulez.configuration as configuration
import src.dimmer.processor as dimmer_processor
import src.dimmer.mqtt_sender as mqtt_sender
import src.output_status.ServiceClient as ServiceClient


logger = log.get_logger('dimmer Module')

# Get config
config = configuration.Configuration()
mqttConfig = config.get_mqtt_config()
serviceConfig = config.get_service_client_config()

# Create client
client = mqtt.Client()
StatusService = ServiceClient.StatusServiceClient(serviceConfig['url'], serviceConfig['port'])
sender = mqtt_sender.MqttSender(client)
processor = dimmer_processor.DimmerActionProcessor(client, sender, StatusService)


def on_connect(connected_client, _, __, rc) -> None:
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))
    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices

    # Receives message from button about dimmer state switch
    subscribe = constants.iRulezTopic + '/' + constants.actionTopic + '/' + constants.dimmerModuleTopic
    logger.debug("Subscribing to " + str(subscribe))
    connected_client.subscribe(subscribe)

    # Receives message from timer module when a dimmer pin should be updated.
    subscribe = constants.iRulezTopic + '/' + constants.actionTopic + '/' + constants.dimmerTimerFired
    logger.debug("Subscribing to " + str(subscribe))
    connected_client.subscribe(subscribe)

    subscribe = constants.iRulezTopic + '/' + constants.dimmerCancelled + '/' + constants.dimmerModuleTopic
    logger.debug("Subscribing to " + str(subscribe))
    connected_client.subscribe(subscribe)

    # # Subscribe to real time dimmer
    # subscribe = constants.arduinoTopic + '/' + constants.actionTopic + '/' + constants.dimmerRealTimeModuleTopic
    # logger.debug("Subscribing to " + str(subscribe))
    # connected_client.subscribe(subscribe)


def on_subscribe(_, __, mid, granted_qos) -> None:
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(_, __, msg) -> None:
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")

    # Find arduino name of topic
    logger.debug(f"Process dimmer message")

    # Check if message is a command message from the button module to start dimming
    if util.is_arduino_dimmer_action_topic(msg.topic):
        processor.process_dimmer_message(msg.payload.decode("utf-8"))
        return

    # Check if message is a timer fired message from the timer module to send the next dimming message
    if util.is_arduino_dimmer_timer_fired_topic(msg.topic):
        processor.process_dimmer_timer_fired(msg.payload.decode("utf-8"))
        return

    if util.is_arduino_dimmer_cancelled_topic(msg.topic):
        processor.process_dimmer_cancelled(msg.payload.decode("utf-8"))
        return

    # # Check if message is for real time dimmer
    # elif util.is_arduino_real_time_dimmer_topic(msg.topic):
    #     dimmer_processor.process_dimmer_real_time_message(msg.payload.decode("utf-8"))

    # Unknown topic
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
