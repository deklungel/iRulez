from enum import IntEnum
import src.irulez.util as util
from abc import ABC, abstractmethod
import src.irulez.log as log
from datetime import datetime, time
from typing import List, Dict, Optional
import src.irulez.constants as constants
import json
from threading import Timer

logger = log.get_logger('domain')


class ArduinoPinType(IntEnum):
    """Represents the purpose of a pin on an arduino"""
    BUTTON = 1
    OUTPUT = 2
    DIMMER = 3


class Pin(ABC):
    """Represents a pin on an arduino"""

    def __init__(self, number: int, pin_type: ArduinoPinType):
        self.number = number
        self.pin_type = pin_type
        self.state = 0

    def get_state(self) -> bool:
        if self.state > 0:
            return True
        return False

    def get_dim_state(self) -> int:
        return self.state


class OutputPin(Pin):
    """Represents a single pin on an arduino"""

    def __init__(self, number: int, parent: str):
        super(OutputPin, self).__init__(number, ArduinoPinType.OUTPUT)
        self.parent = parent


class Arduino:
    """Represents an actual arduino"""

    def __init__(self, name: str, number_of_outputs_pins: int):
        self.name = name
        self.number_of_output_pins = number_of_outputs_pins
        self.output_pins = dict()

    def set_output_pin(self, output_pin: OutputPin):
        self.output_pins[output_pin.number] = output_pin

    def set_output_pins(self, output_pins: List[OutputPin]):
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

    def get_output_pin(self, pin_number: int) -> OutputPin:
        return self.output_pins[pin_number]

    def set_output_pin_status(self, payload: str):
        status = util.convert_hex_to_array(payload, self.number_of_output_pins)
        for pin in self.output_pins.values():
            if int(status[pin.number]) == 1:
                pin.state = 100
            else:
                pin.state = 0


    def set_dimmer_pin_status(self, payload: int, pin):
        self.output_pins[pin].state = payload



class ArduinoConfig:
    """Represents the configuration of all known arduinos"""

    def __init__(self, arduinos: List[Arduino]):
        self.arduinos = arduinos
