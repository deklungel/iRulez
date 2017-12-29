import src.irulez.util as util
import src.irulez.log as log
import lib.paho.mqtt.client as mqtt
import src.irulez.constants as constants
import uuid

logger = log.get_logger('dimmer_mqtt_sender')


class MqttSender:
    def __init__(self, client: mqtt.Client):
        self.__client = client

    def publish_dimming_action_to_timer(self, dimming_action_id: uuid.UUID, delay: int):
        publish_topic = constants.arduinoTopic + '/' + constants.actionTopic + '/' +\
                        constants.dimmerTimerFired + '/' + constants.timerTopic
        topic_name = constants.arduinoTopic + '/' + constants.actionTopic + '/' + constants.dimmerTimerFired
        payload = util.serialize_json({
            'topic': topic_name,
            'payload': dimming_action_id,
            'delay': delay
        })

        self.__client.publish(publish_topic, payload, 0, False)
