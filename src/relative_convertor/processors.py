import src.relative_convertor.mqtt_sender as mqtt_sender
import src.irulez.log as log
import json

logger = log.get_logger('absolute_update_processor')


class RelativeActionProcessor:
    def __init__(self, sender: mqtt_sender.MqttSender):
        self.sender = sender

    def process_relative_action_message(self, payload: str):

        json_object = json.loads(payload)
        self.sender.send_absolute_update(json_object)