import src.relative_convertor.mqtt_sender as mqtt_sender
import src.irulez.log as log
import src.irulez.util as util
import json

logger = log.get_logger('absolute_update_processor')


class RelativeActionProcessor:
    def __init__(self, sender: mqtt_sender.MqttSender, arduinos: {}):
        self.sender = sender
        self.arduinos = arduinos

    def process_relative_action_message(self, payload: str):
        json_object = json.loads(payload)

        arduino = self.arduinos.get(json_object["name"], None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{json_object['name']}'.")
            return

        self.sender.send_absolute_update(arduino, json_object)