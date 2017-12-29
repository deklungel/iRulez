import src.irulez.log as log
from typing import List, Tuple

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

    def increment_step(self) -> None:
        self.__current_step += 1

    @property
    def pins_with_intervals(self) -> List[PinWithIntervals]:
        return self.__pins_to_switch

    @property
    def current_step(self) -> int:
        return self.__current_step

    @property
    def interval_time_between(self) -> int:
        return self.__interval_time_between

    @property
    def arduino_name(self) -> str:
        return self.__arduino_name

    def is_final_step(self) -> bool:
        return self.__current_step == len(self.__pins_to_switch) - 1

    def get_current_pins_with_interval(self) -> List[Tuple[int, int]]:
        to_return = []
        for pin_with_intervals in self.__pins_to_switch:
            to_return.append(Tuple[int, int](pin_with_intervals.pin,
                                             pin_with_intervals.interval_values[self.__current_step]))

        return to_return
