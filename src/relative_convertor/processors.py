import src.relative_convertor.mqtt_sender as mqtt_sender
import src.irulez.log as log
import src.irulez.util as util

logger = log.get_logger('absolute_update_processor')


class RelativeActionProcessor:
    def __init__(self, sender: mqtt_sender.MqttSender):
        self.sender = sender

    def process_relative_action_message(self, payload: str):
        logger.info("Processing " + payload)
        json_object = util.deserialize_json(payload)
        self.sender.send_absolute_update(json_object)
