import src.irulez.util as util
import src.irulez.log as log
import src.output_status.ServiceClient as ServiceClient
from typing import List, Dict
import lib.paho.mqtt.client as mqtt
import src.irulez.constants as constants
import json

logger = log.get_logger('dimmer_mqtt_sender')


class MqttSender:
    def __init__(self, client: mqtt.Client, status_service: ServiceClient.StatusServiceClient):
        self.client = client

    def publish_dim_message(self,pin: int, name: str,  value: int, dim_value: float, speed: int, direction_up: bool):
        publish_topic = constants.arduinoTopic + '/'+ constants.dimmerTopic + '/' + constants.timerTopic
        topic_name = constants.arduinoTopic + '/' + name + '/' + constants.actionTopic
        payload = json.dumps(
            {
                'pin': pin,
                'initial_value': value,
                'dim_value': dim_value,
                'speed': speed,
                'directionUP': direction_up,
                'topic': topic_name
            }
        )

        self.client.publish(publish_topic, payload, 0, False)
