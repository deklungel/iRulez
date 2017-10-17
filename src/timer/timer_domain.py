from src.irulez.domain import OutputPin
from typing import List, Dict, Optional
import src.irulez.log as log
from abc import ABC, abstractmethod

logger = log.get_logger('timer_domain')

# todo: create abstracte timer


class Timer(ABC):
    def __init__(self, name: str, topic: str):
        self.name = name
        self.topic = topic


class RelativeActionTimer(Timer):
    def __init__(self, name: str, topic: str, output_pins_on: List[int], output_pins_off: List[int]):
        super(RelativeActionTimer, self).__init__(name, topic)
        self.output_pins_on = output_pins_on
        self.output_pins_off = output_pins_off

    def check_pins(self, json_object: []):
        self.check_remove_pin(json_object["on"])
        self.check_remove_pin(json_object["off"])

    def check_remove_pin(self, jsonobject: []):
        for pin in jsonobject:
            if pin in self.output_pins_on:
                self.output_pins_on.remove(pin)
                logger.debug(f"on pin {pin} has been deleted from timer")
            if pin in self.output_pins_off:
                self.output_pins_off.remove(pin)
                logger.debug(f"off pin {pin} has been deleted from timer")

    def check_empty_timer(self):
        return len(self.output_pins_on) == 0 and len(self.output_pins_on) == 0



