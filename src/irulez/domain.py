from enum import Enum
import src.irulez.util as util


class ArduinoPinType(Enum):
    """Represents the purpose of a pin on an arduino"""
    BUTTON = 1
    RELAY = 2
    DIMMER = 3


class ActionType(Enum):
    """Represents what should happen. Toggle --> Relais H <-> L, On --> Relay H, Off --> Relay L, Follow_Button --> when button pressed -> relay H, dimmer --> dimmer"""
    TOGGLE = 1
    ON = 2
    OFF = 3
    FOLLOW_BUTTON = 4
    DIMMER = 5


class ActionTriggerType(Enum):
    """Represents when a action need to be executed"""
    Immediately = 1
    AfterRelease = 2
    LongDown = 3
    DubbleTap = 4
    TrippleTap = 5


class ActionTrigger:
    def __init__(self, type: ActionTriggerType):
        self.type = type

    def get_actionTrigger(self):
        return  self.type


class ImmediatelyActionTrigger(ActionTrigger):
    def __init__(self):
        super(ImmediatelyActionTrigger, self).__init__(ActionTriggerType.Immediately)


class AfterReleaseActionTrigger(ActionTrigger):
    def _init_(self):
        super(AfterReleaseActionTrigger, self).__init__(ActionTriggerType.AfterRelease)


class LongDownActionTrigger(ActionTrigger):
    def _init_(self, SecDown: int):
        super(LongDownActionTrigger, self).__init__(ActionTriggerType.LongDown)
        self.SecDown = SecDown


class DubbleTapActionTrigger(ActionTrigger):
    def _init_(self, TimeBetweenTap: int):
        super(DubbleTapActionTrigger, self).__init__(ActionTriggerType.DubbleTap)
        self.TimeBetweenTap = TimeBetweenTap


class TrippleTapActionTrigger(ActionTrigger):
    def _init_(self, TimeBetweenTap: int):
        super(TrippleTapActionTrigger, self)._init_(ActionTriggerType.TrippleTap)
        self.TimeBetweenTap = TimeBetweenTap


class OutputPin:
    """Represents a single pin on an arduino"""
    def __init__(self, number: int, pin_type: ArduinoPinType, state=False):
        self.number = number
        self.type = pin_type
        self.state = state


class Notification:
    def __init__(self,enabled: False):
        self.enabled = enabled

class MailNotification(Notification):
    def __init__(self, email: str, enabled= False):
        super(MailNotification, self).__init__(enabled)
        self.email = email

class TelegramNotification(Notification):
    def __init__(self, token: str, enabled= False):
        super(TelegramNotification, self).__init__(enabled)
        self.token = token

class ButtonPin:
    """Represents a single input pin on an arduino"""

    def __init__(self, number: int, pin_type: ArduinoPinType, state:False, actions: list):
        self.number = number
        self.type = pin_type
        self.state = state
        all(isinstance(el, Action) for el in actions)
        self.actions = actions

    def set_button_pin_actions(self, actions: list):
        self.actions = actions

class Action:
        "Represents a singe action"
        def __init__(self,trigger: ActionTrigger, type: ActionType, delay: int, relay_pins: list, notification: Notification):
            self.trigger = trigger
            self.type = type
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
