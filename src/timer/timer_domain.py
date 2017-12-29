from typing import List, Dict
import src.irulez.log as log
from abc import ABC

logger = log.get_logger('timer_domain')

# todo: create abstract timer


class Timer(ABC):
    def __init__(self, topic: str):
        self.topic = topic


class IndividualAction:
    """Represents the actions on pins that have to happen on a single arduino"""
    def __init__(self,
                 arduino_name: str,
                 mqtt_topic: str,
                 delay: int,
                 pin_numbers_on: List[int],
                 pin_numbers_off: List[int]):
        self.name = arduino_name
        self.topic = mqtt_topic
        self.delay = delay
        self.pin_numbers_on = pin_numbers_on
        self.pin_numbers_off = pin_numbers_off

    def add_pin_on(self, pin_number: int):
        self.pin_numbers_on.append(pin_number)

    def add_pin_off(self, pin_number: int):
        self.pin_numbers_off.append(pin_number)

    def has_values_on(self) -> bool:
        if len(self.pin_numbers_on) > 0:
            return True
        return False

    def has_values_off(self) -> bool:
        if len(self.pin_numbers_off) > 0:
            return True
        return False


class RelativeActionTimer(Timer):
    def __init__(self, name: str, topic: str, output_pins_on: List[int], output_pins_off: List[int]):
        super(RelativeActionTimer, self).__init__(topic)
        self.name = name
        self.output_pins_on = output_pins_on
        self.output_pins_off = output_pins_off

    def check_pins(self, json_object: Dict):
        self.check_remove_pin(json_object["on"])
        self.check_remove_pin(json_object["off"])

    def check_remove_pin(self, json_object: List[int]):
        for pin in json_object:
            if pin in self.output_pins_on:
                self.output_pins_on.remove(pin)
                logger.debug(f"on pin {pin} has been deleted from timer")
            if pin in self.output_pins_off:
                self.output_pins_off.remove(pin)
                logger.debug(f"off pin {pin} has been deleted from timer")

    def check_empty_timer(self) -> bool:
        return len(self.output_pins_on) == 0 and len(self.output_pins_on) == 0


class DefaultTimer(Timer):
    def __init__(self, topic: str, payload: str):
        super().__init__(topic)
        self.__payload = payload

    @property
    def payload(self) -> str:
        return self.__payload
