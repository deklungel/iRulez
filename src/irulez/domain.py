from enum import Enum


class ArduinoPinType(Enum):
    """Represents the purpose of a pin on an arduino"""
    BUTTON = 1
    RELAY = 2
    DIMMER = 3


class ArduinoPin:
    """Represents a single pin on an arduino"""
    def __init__(self, number: int, pin_type: ArduinoPinType, state=False):
        self.number = number
        self.type = pin_type
        self.state = state


class Arduino:
    """Represents an actual arduino"""
    def __init__(self, name: str, pins: list):
        # Check that all elements in our list are actual ArduinoPin objects
        # This check is completely unnecessary, but gives us some assurances
        all(isinstance(el, ArduinoPin) for el in pins)
        self.name = name
        self.pins = {}
        for pin in pins:
            self.pins[pin.number] = pin

    def get_relay_status(self):
        """Gets the status array of the pins of this arduino"""
        # Initialize empty state array
        pin_states = [0]*16
        # Loop over all pins and set their state in the array
        for pin in self.pins:
            pin_states[pin.number] = 1 if pin.state else 0

        # Convert to a string
        status = ''.join(pin_states)
        # Convert to hex
        status = hex(int(status))
        return status


class ArduinoConfig:
    """Represents the configuration of all known arduinos"""
    def __init__(self, arduinos: list):
        self.arduinos = arduinos


class MqttConfig:
    """Represents the configuration of the mqtt service"""
    def __init__(self, address: str, port: int, username: str, password: str):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
