import json
from typing import Dict, List

import src.button.domain as irulez_domain
import src.irulez.constants as constants
import src.irulez.log as log

logger = log.get_logger('button_mqtt_sender')


class MqttSender:
    def __init__(self, client, arduinos: {}):
        self.client = client
        self.arduinos = arduinos

    def publish_relative_action(self, json_list: Dict[str, List[irulez_domain.IndividualAction]]):
        for name in json_list:
            for i in range(len(json_list[name])):
                topic_name = constants.arduinoTopic + '/' + name + '/' + constants.actionTopic
                publish_topic = constants.arduinoTopic + '/' + constants.actionTopic + '/' + constants.relativeTopic
                if json_list[name][i].delay != 0:
                    topic_name = topic_name + '/' + constants.relativeTopic
                    publish_topic = publish_topic + '/' + constants.timerTopic

                payload = json.dumps(
                    {
                        "name": name,
                        "topic": topic_name,
                        "on": json_list[name][i].pin_numbers_on, "off": json_list[name][i].pin_numbers_off,
                        "delay": json_list[name][i].delay})

                logger.debug(f"Publishing: {publish_topic}{payload}")
                self.client.publish(publish_topic, payload, 0, False)

    def publish_message_to_button_processor(self, timer: List[object]):
        arduino_name = timer[0]
        button_pin = timer[1]
        seconds_down = timer[2]
        clicks = timer[3]

        publish_topic = constants.arduinoTopic + '/' + constants.buttonTimerFiredTopic
        payload = json.dumps(
            {
                "name": arduino_name,
                "button_pin": button_pin,
                "seconds_down": seconds_down,
                "clicks": clicks
            }
        )


        logger.debug(f"Publishing: {publish_topic}{payload}")
        self.client.publish(publish_topic, payload, 0, False)

    def publish_multiclick_message_to_button_processor(self, multiclick: List[object]):
        arduino_name = multiclick[0]
        button_pin = multiclick[1]
        clicks = multiclick[2]

        publish_topic = constants.arduinoTopic + '/' + constants.buttonMulticlickFiredTopic
        payload = json.dumps(
            {
                "name": arduino_name,
                "button_pin": button_pin,
                "clicks": clicks
            }
        )

        logger.debug(f"Publishing: {publish_topic}{payload}")
        self.client.publish(publish_topic, payload, 0, False)

    def publish_notification(self, topic: str, payload: Dict[str, object]):
        logger.debug(f"Publishing: {topic}{payload}")
        self.client.publish(topic, payload, 0, False)