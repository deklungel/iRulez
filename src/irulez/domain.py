from enum import Enum
import src.irulez.util as util
from abc import ABC


class ArduinoPinType(Enum):
    """Represents the purpose of a pin on an arduino"""
    BUTTON = 1
    RELAY = 2
    DIMMER = 3


class ActionType(Enum):
    """Represents what should happen.
        Toggle --> Relay H <-> L,
        On --> Relay H,
        Off --> Relay L,
        Follow_Button --> when button pressed -> relay H,
        dimmer --> dimmer"""
    TOGGLE = 1
    ON = 2
    OFF = 3
    FOLLOW_BUTTON = 4
    DIMMER = 5
    DOORPHONE = 6


class ActionTriggerType(Enum):
    """Represents when a action need to be executed"""
    IMMEDIATELY = 1
    AFTER_RELEASE = 2
    LONG_DOWN = 3
    DOUBLE_TAP = 4
    TRIPLE_TAP = 5


class ActionTrigger(ABC):
    def __init__(self, trigger_type: ActionTriggerType):
        self.trigger_type = trigger_type

    def get_action_trigger_type(self):
        return self.trigger_type


class ImmediatelyActionTrigger(ActionTrigger):
    def __init__(self):
        super(ImmediatelyActionTrigger, self).__init__(ActionTriggerType.IMMEDIATELY)


class AfterReleaseActionTrigger(ActionTrigger):
    def _init_(self):
        super(AfterReleaseActionTrigger, self).__init__(ActionTriggerType.AFTER_RELEASE)


class LongDownActionTrigger(ActionTrigger):
    def _init_(self, seconds_down: int):
        super(LongDownActionTrigger, self).__init__(ActionTriggerType.LONG_DOWN)
        self.seconds_down = seconds_down


class DoubleTapActionTrigger(ActionTrigger):
    def _init_(self, time_between_tap: int):
        super(DoubleTapActionTrigger, self).__init__(ActionTriggerType.DOUBLE_TAP)
        self.time_between_tap = time_between_tap


class TripleTapActionTrigger(ActionTrigger):
    def _init_(self, time_between_tap: int):
        super(TripleTapActionTrigger, self).__init__(ActionTriggerType.TRIPLE_TAP)
        self.time_between_tap = time_between_tap


class Pin(ABC):
    """Represents a pin on an arduino"""
    def __init__(self, number: int, pin_type: ArduinoPinType, state=False):
        self.number = number
        self.pin_type = pin_type
        self.state = state


class OutputPin(Pin):
    """Represents a single pin on an arduino"""
    def __init__(self, number: int, state=False):
        super(OutputPin, self).__init__(number, ArduinoPinType.RELAY, state)


class ButtonPin(Pin):
    """Represents a single input pin on an arduino"""

    def __init__(self, number: int, actions: list, state=False):
        super(ButtonPin, self).__init__(number, ArduinoPinType.BUTTON, state)
        all(isinstance(el, Action) for el in actions)
        self.actions = actions

    def set_button_pin_actions(self, actions: list):
        self.actions = actions


class Notification(ABC):
    def __init__(self, enabled: False):
        self.enabled = enabled


class MailNotification(Notification):
    def __init__(self, email: str, enabled=False):
        super(MailNotification, self).__init__(enabled)
        self.email = email


class TelegramNotification(Notification):
    def __init__(self, token: str, enabled=False):
        super(TelegramNotification, self).__init__(enabled)
        self.token = token


class Action:
        """Represents a singe action"""
        def __init__(self,
                     trigger: ActionTrigger,
                     action_type: ActionType,
                     delay: int,
                     relay_pins: list,
                     notification: Notification):
            self.trigger = trigger
            self.action_type = action_type
            self.delay = delay
            all(isinstance(el, OutputPin) for el in relay_pins)
            self.relay_pins = relay_pins
            self.notification = notification


class Arduino:
    """Represents an actual arduino"""

    def __init__(self, name: str, number_of_relay_pins: int, number_of_button_pins: int):
        self.name = name
        self.number_of_relay_pins = number_of_relay_pins
        self.number_of_button_pins = number_of_button_pins
        self.relay_pins = {}
        self.button_pins = {}

    def set_relay_pins(self, relay_pins: list):
        # Check that all elements in our list are actual OutputPin objects
        # This check is completely unnecessary, but gives us some assurances
        all(isinstance(el, OutputPin) for el in relay_pins)
        for pin in relay_pins:
            self.relay_pins[pin.number] = pin

    def set_button_pins(self, button_pins: list):
        # Check that all elements in our list are actual button_pins objects
        all(isinstance(el, ButtonPin) for el in button_pins)
        for pin in button_pins:
            self.button_pins[pin.number] = pin

    def get_relay_status(self) -> str:
        """Gets the status array of the relay_pins of this arduino"""
        # Initialize empty state array
        pin_states = [0] * self.number_of_relay_pins
        # Loop over all relay_pins and set their state in the array
        for pin in self.relay_pins.values():
            pin_states[pin.number] = 1 if pin.state else 0

        # convert array to hex string
        return util.convert_array_to_hex(pin_states)


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
