import src.irulez.constants as constants
import src.irulez.log as log
import json
import src.timer.timer_domain as timer_domain

logger = log.get_logger('timer_mqtt_sender')


class MqttSender:
    def __init__(self, client):
        self.client = client

    def publish_relative_action(self, individual_action):
        payload = \
            json.dumps({"name": individual_action.name,
                        "topic": constants.arduinoTopic + '/' + individual_action.name + '/' + constants.actionTopic,
                        "on": individual_action.pin_numbers_on, "off": individual_action.pin_numbers_off,
                        "delay": individual_action.delay})

        logger.debug(f"Publishing: {individual_action.topic}{payload}")
        self.client.publish(individual_action.topic, payload, 0, False)

    def publish_dim_action(self, action_dim_timer: timer_domain.RelativeActionDimTimer ):
        payload = action_dim_timer.value
        topic = action_dim_timer.topic
        logger.debug(f"Publishing: {individual_action.topic}{payload}")
        self.client.publish(topic, payload, 0, False)