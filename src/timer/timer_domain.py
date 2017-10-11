from src.irulez.domain import OutputPin
from typing import List, Dict, Optional

class Timer:
    def __init__(self, id: int, delay: int, output_pins: List[OutputPin]):
        self.id = id
        self.delay = delay
        self.output_pins = output_pins


    def checkOutputPin(self,pinNumber: int):
        for pin in self.output_pins.value():
            if pin.number == pinNumber:
                return id
        return None