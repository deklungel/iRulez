import src.irulez.constants as constants
import src.irulez.log as log
import json
from typing import List, Dict, Optional
import src.irulez.domain as domain

logger = log.get_logger('button_mqtt_sender')


class MqttSender:
    def __init__(self, client, arduinos: {}):
        self.client = client
        self.arduinos = arduinos

    def publish_relative_action(self, json_list: Dict[str, domain.IndividualAction]):
        for name in json_list:
            for i in range(len(json_list[name])):
                topic_name = constants.arduinoTopic + '/' + name + '/' + constants.actionTopic
                publish_topic = constants.arduinoTopic + '/' + constants.actionTopic + '/' + constants.relative
                if json_list[name][i].delay != 0:
                    topic_name = topic_name + '/' + constants.relative
                    publish_topic = publish_topic + '/' + constants.timer

                payload = json.dumps(
                    {
                        "name": name,
                        "topic": topic_name,
                        "on": json_list[name][i].pin_numbers_on, "off": json_list[name][i].pin_numbers_off,
                        "delay": json_list[name][i].delay})

                logger.debug(f"Publishing: {publish_topic}{payload}")
                self.client.publish(publish_topic, payload, 0, False)




