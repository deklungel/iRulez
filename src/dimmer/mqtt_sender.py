import src.irulez.util as util
import src.irulez.topic_factory as topic_factory
import src.irulez.log as log
import paho.mqtt.client as mqtt
import uuid

logger = log.get_logger('dimmer_mqtt_sender')


class MqttSender:
    def __init__(self, client: mqtt.Client):
        self.__client = client

    def publish_dimming_action_to_timer(self, dimming_action_id: uuid.UUID, delay: int):
        publish_topic = topic_factory.create_timer_dimmer_timer_fired_topic()
        topic_name = topic_factory.create_timer_dimmer_timer_fired_response_topic()
        payload = util.serialize_json({
            'topic': topic_name,
            'payload': str(dimming_action_id),
            'delay': delay
        })

        logger.debug(f"Publishing: {publish_topic}{payload}")
        self.__client.publish(publish_topic, payload, 0, False)

    def publish_dimming_action_to_arduino(self, arduino_name: str, pin_number: int, dim_value: int):
        publish_topic = topic_factory.create_arduino_dim_action_topic(arduino_name, pin_number)
        logger.debug(f"Publishing: {publish_topic} / {dim_value}")
        self.__client.publish(publish_topic, dim_value, 0, False)
