import src.communication.mqtt_sender as mqtt_sender
import src.irulez.log as log
import src.irulez.util as util

logger = log.get_logger('absolute_update_processor')


class RelativeActionProcessor:
    def __init__(self, sender: mqtt_sender.MqttSender, arduinos: {}):
        self.sender = sender
        self.arduinos = arduinos

    def process_relative_action_message(self, name: str, payload: str):
        logger.debug(f"payload '{payload}'")
        on, off = payload.split('|')

        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return

        self.sender.send_absolute_update(name, util.convert_hex_to_array(on, arduino.number_of_output_pins), util.convert_hex_to_array(off, arduino.number_of_output_pins))