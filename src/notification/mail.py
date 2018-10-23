import lib.paho.mqtt.client as mqtt
import src.irulez.configuration as configuration
import src.irulez.constants as constants
import src.irulez.log as log
import src.notification.processor as processor

logger = log.get_logger('mail')

# Create client
client = mqtt.Client()

config = configuration.Configuration()
mailConfig = config.authenticate_SMTP_config()

# Create gmail Processor
mail = processor.AuthenticateSMTPProcessor(mailConfig['username'],
                                           mailConfig['password'],
                                           int(mailConfig['port']),
                                           mailConfig['url'])


def on_connect(connected_client, _, __, rc) -> None:
    """Callback function for when the mqtt client is connected."""
    logger.info("Connected client with result code " + str(rc))
    # Subscribe in on_connect callback to automatically re-subscribe if the connection was lost
    # Subscribe to all arduino hexnumber actions
    # '+' means single level wildcard. '#' means multi level wildcard.
    # See http://www.hivemq.com/blog/mqtt-essentials-part-5-mqtt-topics-best-practices
    topic = str(constants.iRulezTopic) + "/" + str(constants.notificationTopic) + "/" + str(constants.mailTopic)
    logger.debug("Subscribing to " + str(topic))
    connected_client.subscribe(str(topic))


def on_subscribe(_, __, mid, granted_qos) -> None:
    logger.debug("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(_, __, msg) -> None:
    """Callback function for when a new message is received."""
    logger.debug(f"Received message {msg.topic}: {msg.payload}")
    mail.send_mail(msg.payload.decode("utf-8"))


# Set callback functions
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# Connect
mqttConfig = config.get_mqtt_config()

client.username_pw_set(mqttConfig['username'], mqttConfig['password'])
client.connect(mqttConfig['ip'], int(mqttConfig['port']), 60)

logger.info("Starting loop forever")
# Blocking class that loops forever
# Also handles reconnecting
client.loop_forever()
