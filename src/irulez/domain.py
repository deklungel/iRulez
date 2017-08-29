from enum import Enum


class ArduinoPinType(Enum):
    """Represents the purpose of a pin on an arduino"""
    BUTTON = 1
    RELAY = 2
    DIMMER = 3


class ArduinoPin:
    """Represents a single pin on an arduino"""
    def __init__(self, number: int, pin_type: ArduinoPinType):
        self.number = number
        self.type = pin_type
