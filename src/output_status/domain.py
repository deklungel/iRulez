from enum import IntEnum
import src.irulez.util as util
from abc import ABC
import src.irulez.log as log
import src.irulez.constants as constants
from typing import List, Optional, Dict

logger = log.get_logger('domain')


class ArduinoPinType(IntEnum):
    """Represents the purpose of a pin on an arduino"""
    BUTTON = 1
    OUTPUT = 2
    DIMMER = 3


class Pin(ABC):
    """Represents a pin on an arduino"""

    def __init__(self, number: int, pin_type: ArduinoPinType):
        self.__number = number
        self.__pin_type = pin_type
        self.__state = 0
        self.__direction = constants.dim_direction_up

    @property
    def state(self) -> bool:
        if self.__state > 0:
            return True
        return False

    @state.setter
    def state(self, state: int) -> None:
        self.__state = state

    @property
    def number(self) -> int:
        return self.__number

    @property
    def dim_state(self) -> int:
        return self.__state

    @property
    def direction(self) -> Optional[str]:
        return self.__direction

    @direction.setter
    def direction(self, direction: str) -> None:
        self.__direction = direction


class OutputPin(Pin):
    """Represents a single pin on an arduino"""

    def __init__(self, number: int, parent: str):
        super(OutputPin, self).__init__(number, ArduinoPinType.OUTPUT)
        self.parent = parent


class DimmerLightValue:
    """Class for keeping the last_light_value of a dimmer_id"""

    def __init__(self, id: int, last_light_value: int):
        self.__last_light_value = last_light_value
        self.__id = id

    @property
    def id(self) -> int:
        return self.__id

    @property
    def last_light_value(self) -> int:
        return self.__last_light_value

    @last_light_value.setter
    def last_light_value(self, last_light_value: int) -> None:
        self.__last_light_value = last_light_value


class Arduino:
    """Represents an actual arduino"""

    def __init__(self, name: str, number_of_outputs_pins: int):
        self.name = name
        self.number_of_output_pins = number_of_outputs_pins
        self.__output_pins = dict()

    @property
    def output_pins(self) -> Dict[int, OutputPin]:
        return self.__output_pins

    def set_output_pin(self, output_pin: OutputPin) -> None:
        self.output_pins[output_pin.number] = output_pin

    def set_output_pins(self, output_pins: List[OutputPin]) -> None:
        for pin in output_pins:
            self.output_pins[pin.number] = pin

    def get_output_pin_status(self) -> str:
        """Gets the status array of the output_pins of this arduino"""
        # Initialize empty state array
        pin_states = [0] * self.number_of_output_pins
        # Loop over all output_pins and set their state in the array
        for pin in self.output_pins.values():
            pin_states[pin.number] = 1 if pin.state else 0

        # convert array to hex string
        return util.convert_array_to_hex(pin_states)

    def get_output_dim_pin_status(self) -> str:
        to_return = ''
        for pin in self.output_pins.values():
            to_return += str(pin.dim_state) + ' '

        return to_return

    def get_output_pin(self, pin_number: int) -> OutputPin:
        return self.output_pins[pin_number]

    def set_output_pin_status(self, payload: str) -> None:
        status = util.convert_hex_to_array(payload, self.number_of_output_pins)
        for pin in self.output_pins.values():
            if int(status[pin.number]) == 1:
                pin.state = 100
            else:
                pin.state = 0

    def set_dimmer_pin_status(self, payload: int, pin_number: int) -> None:
        pin = self.output_pins[pin_number]
        if pin.dim_state - payload > 0:
            pin.direction = constants.dim_direction_down
        elif pin.dim_state - payload < 0:
            pin.direction = constants.dim_direction_up
        self.output_pins[pin_number].state = payload


class ArduinoConfig:
    """Represents the configuration of all known arduinos"""

    def __init__(self, arduinos: List[Arduino]):
        self.arduinos = arduinos
