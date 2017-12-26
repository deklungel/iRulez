import src.irulez.log as log
from typing import List

logger = log.get_logger('dimmer_domain')


class ButtonLow:
    def __init__(self, button_numbers: List[int] , number_of_pins: int):
        self.button_numbers = button_numbers
        self.number_of_pins = number_of_pins

    def cleanup(self, button_pins: List[int]):
        for button_pin in button_pins:
            self.button_numbers.remove(button_pin)
            logger.debug(f"Button pin with number {button_pin} removed from list.")





