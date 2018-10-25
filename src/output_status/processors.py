import src.irulez.log as log
import src.irulez.util as util

logger = log.get_logger('service_processor')


class ServiceProcessor:
    def __init__(self, arduinos: {}):
        self.arduinos = arduinos

    def update_arduino_output_pins(self, name: str, payload: str):
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return
        logger.debug(f"Board with name '{name}' found")
        arduino.set_output_pin_status(payload)
        logger.debug(f"relay status HEX: '{arduino.get_output_pin_status()}'.")

    def update_arduino_dimmer_pins(self, name: str, dimmer_pin: int, payload: str):
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return
        logger.debug(f"Board with name '{name}' found")
        arduino.set_dimmer_pin_status(int(payload), dimmer_pin)
        logger.debug(f"dimmer values: '{arduino.get_output_pin_status()}'.")

    def update_last_light_value(self, payload: str):
        json_object = util.deserialize_json(payload)
        arduino_name = util.get_str_from_json_object(json_object, 'arduino_name')
        dimmer_id = util.get_int_from_json_object(json_object, 'dimmer_id')
        last_light_value = util.get_int_from_json_object(json_object, 'last_light_value')

        arduino = self.arduinos.get(arduino_name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{arduino_name}'.")
            return
        arduino.set_dimmer_pin_last_light_value(dimmer_id, last_light_value)
