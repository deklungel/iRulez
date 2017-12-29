import src.irulez.log as log
import src.irulez.constants as constants
import src.irulez.util as util
import lib.paho.mqtt.client as mqtt
import src.irulez.configuration as configuration
import src.timer.processor as timer_processor
import src.timer.mqtt_sender as mqtt_sender

logger = log.get_logger('timer')

# Create client
client = mqtt.Client()
sender = mqtt_sender.MqttSender(client)
TimeProcessor = timer_processor.TimerProcessor(sender)


def on_connect(connected_client, _, __, rc):
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))
    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices

    # When the button module sends a timed relay action to the relative convertor module
    topic = "{0}/{1}/{2}/{3}".format(str(constants.arduinoTopic), str(constants.actionTopic),
                                     str(constants.relativeTopic), str(constants.timerTopic))
    logger.debug("Subscribing to " + str(topic))
    connected_client.subscribe(str(topic))

    # When the button module sends a timed dim action to the dimmer module
    topic = "{0}/{1}/{2}/{3}".format(str(constants.arduinoTopic), str(constants.actionTopic),
                                     str(constants.dimmerModuleTopic), str(constants.timerTopic))
    logger.debug("Subscribing to " + str(topic))
    connected_client.subscribe(str(topic))

    # When the dimmer module sends a message to itself
    topic = constants.arduinoTopic + '/' + constants.actionTopic + '/' + constants.dimmerTimerFired + '/' + \
        constants.timerTopic
    logger.debug("Subscribing to " + str(topic))
    connected_client.subscribe(str(topic))


def on_subscribe(_, __, mid, granted_qos):
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(_, __, msg):
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")

    # Check if the topic is an action for sending a timed message to the relative convertor module
    if util.is_arduino_timer_action_topic(msg.topic):
        logger.debug(f"Process the timer action")
        TimeProcessor.process_timer_action_request(msg.payload.decode("utf-8"))
        return

    # Check if the topic is relative action. Used to cancel running timers
    if util.is_arduino_relative_action_topic(msg.topic):
        logger.debug(f"Check if pin is used in timer")
        TimeProcessor.check_output_pin(msg.payload.decode("utf-8"))
        return

    # Check if the topic is an action for sending a timed dim message to the arduino. Sent by the dimmer module
    if util.is_arduino_dimmer_timer_fired_topic_for_timer_module(msg.topic):
        logger.debug(f"Process the timer dimmer action")
        TimeProcessor.process_default_timer_request(msg.payload.decode("utf-8"))
        return

    logger.warning(f"Topic '{msg.topic}' is of no interest to us. Are we subscribed to too much?")
    # Unknown topic
    return


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
