import src.irulez.log as log


logger = log.get_logger('service_processor')

class service_processor:
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
