from src.irulez.domain import OutputPin
from typing import List, Dict, Optional
import src.irulez.log as log

logger = log.get_logger('timer_domain')

class Timer:
    def __init__(self, name:str, output_pins_on: List[int], output_pins_off: List[int]):
        self.name = name
        self.output_pins_on = output_pins_on
        self.output_pins_off = output_pins_off

    def checkPins(self, jsonobject: []):

        self.checkAndRemovePin(jsonobject["on"])
        self.checkAndRemovePin(jsonobject["off"])

    def checkAndRemovePin(self, jsonobject: []):
        for pin in jsonobject:
            if pin in self.output_pins_on:
                self.output_pins_on.remove(pin)
                logger.debug(f"on pin {pin} has been deleted from timer")
            if pin in self.output_pins_off:
                self.output_pins_off.remove(pin)
                logger.debug(f"off pin {pin} has been deleted from timer")

    def checkEmptyTimer(self):
        return (len(self.output_pins_on) == 0 and len(self.output_pins_on) == 0)



