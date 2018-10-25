import src.irulez.log as log
import src.irulez.util as util
from typing import Dict
import src.output_status.domain as domain

logger = log.get_logger('service_processor')


class ServiceProcessor:
    def __init__(self, arduinos: Dict[str, domain.Arduino], dimmer_light_values: Dict[int, domain.DimmerLightValue]):
        self.__arduinos = arduinos
        self.__dimmer_light_values = dimmer_light_values

    @property
    def arduinos(self) -> Dict[str, domain.Arduino]:
        return self.__arduinos

    @property
    def dimmer_light_values(self) -> Dict[int, domain.DimmerLightValue]:
        return self.__dimmer_light_values

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
        logger.debug(f"dimmer values: '{arduino.get_output_dim_pin_status()}'.")

    def update_last_light_value(self, payload: str):
        json_object = util.deserialize_json(payload)
        dimmer_id = util.get_int_from_json_object(json_object, 'dimmer_id')
        last_light_value = util.get_int_from_json_object(json_object, 'last_light_value')

        dimmer_light_value = self.dimmer_light_values.get(dimmer_id, None)
        if dimmer_light_value is None:
            dimmer_light_value = domain.DimmerLightValue(dimmer_id, last_light_value)
            self.dimmer_light_values[dimmer_id] = dimmer_light_value
        else:
            dimmer_light_value.last_light_value = last_light_value
