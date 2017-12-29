import src.irulez.log as log
from typing import List

logger = log.get_logger('dimmer_domain')


class ButtonLow:
    def __init__(self, button_numbers: List[int], number_of_pins: int):
        self.button_numbers = button_numbers
        self.number_of_pins = number_of_pins

    def cleanup(self, button_pins: List[int]):
        for button_pin in button_pins:
            self.button_numbers.remove(button_pin)
            logger.debug(f"Button pin with number {button_pin} removed from list.")


class PinWithIntervals:
    def __init__(self, pin: int, interval_values: List[int]):
        self.__pin = pin
        self.__interval_values = interval_values

    @property
    def pin(self) -> int:
        return self.__pin

    @property
    def interval_values(self) -> List[int]:
        return self.__interval_values


class DimmingAction:
    def __init__(self,
                 arduino_name: str,
                 interval_time_between: int):
        self.__arduino_name = arduino_name
        self.__pins_to_switch = []
        self.__interval_time_between = interval_time_between
        self.__current_step = 0

    def add_pin(self, pin_with_intervals: PinWithIntervals):
        self.__pins_to_switch.append(pin_with_intervals)

    def increment_step(self):
        self.__current_step += 1

    @property
    def pins_with_intervals(self) -> List[PinWithIntervals]:
        return self.__pins_to_switch

    @property
    def current_step(self):
        return self.__current_step

    def is_final_step(self):
        return self.__current_step == len(self.__pins_to_switch) - 1
