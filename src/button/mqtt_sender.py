import src.irulez.constants as constants
import src.irulez.log as log
import json

logger = log.get_logger('button_mqtt_sender')


class MqttSender:
    def __init__(self, client, arduinos: {}):
        self.client = client
        self.arduinos = arduinos

    def publish_relative_action(self, json_list: {}):
        for name in json_list:
            for i in range(len(json_list[name])):
                if json_list[name][i].delay == 0:
                    payload = json.dumps(
                        {
                            "name": name,
                            "topic": constants.arduinoTopic + '/' + name + '/' + constants.actionTopic,
                            "on": json_list[name][i].pin_numbers_on, "off": json_list[name][i].pin_numbers_off,
                            "delay": json_list[name][i].delay})
                    topic = constants.arduinoTopic + '/' + constants.actionTopic + '/' + constants.relative
                else:
                    payload = json.dumps(
                        {
                            "name": name,
                            "topic": constants.arduinoTopic + '/' + name + '/' + constants.actionTopic + '/' + constants.relative,
                            "on": json_list[name][i].pin_numbers_on, "off": json_list[name][i].pin_numbers_off,
                            "delay": json_list[name][i].delay})
                    topic = constants.arduinoTopic + '/' + constants.actionTopic + '/' + constants.relative + '/' + constants.timer

                logger.debug(f"Publishing: {topic}{payload}")
                self.client.publish(topic, payload, 0, False)




