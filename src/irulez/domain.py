from enum import Enum
import src.irulez.util as util
from abc import ABC, abstractmethod
import src.irulez.log as log

logger = log.get_logger('domain')


class ArduinoPinType(Enum):
    """Represents the purpose of a pin on an arduino"""
    BUTTON = 1
    OUTPUT = 2
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
    DOOR_PHONE = 6


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

    @abstractmethod
    def should_trigger(self, value: bool):
        pass


class ImmediatelyActionTrigger(ActionTrigger):
    def should_trigger(self, value: bool):
        return value

    def __init__(self):
        super(ImmediatelyActionTrigger, self).__init__(ActionTriggerType.IMMEDIATELY)


class AfterReleaseActionTrigger(ActionTrigger):
    def should_trigger(self, value: bool):
        return not value

    def _init_(self):
        super(AfterReleaseActionTrigger, self).__init__(ActionTriggerType.AFTER_RELEASE)


class LongDownActionTrigger(ActionTrigger):
    def should_trigger(self, value: bool):
        NotImplementedError
        pass

    def _init_(self, seconds_down: int):
        super(LongDownActionTrigger, self).__init__(ActionTriggerType.LONG_DOWN)
        self.seconds_down = seconds_down


class DoubleTapActionTrigger(ActionTrigger):
    def should_trigger(self, value: bool):
        NotImplementedError
        pass

    def _init_(self, time_between_tap: int):
        super(DoubleTapActionTrigger, self).__init__(ActionTriggerType.DOUBLE_TAP)
        self.time_between_tap = time_between_tap


class TripleTapActionTrigger(ActionTrigger):
    def should_trigger(self, value: bool):
        NotImplementedError
        pass

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

    def __init__(self, number: int, parent: str, state=False):
        super(OutputPin, self).__init__(number, ArduinoPinType.OUTPUT, state)
        self.parent = parent


class ButtonPin(Pin):
    """Represents a single input pin on an arduino"""

    def __init__(self, number: int, actions: list, state=False):
        super(ButtonPin, self).__init__(number, ArduinoPinType.BUTTON, state)
        all(isinstance(el, Action) for el in actions)
        self.actions = actions

    def set_button_pin_actions(self, actions: list):
        self.actions = actions

    def get_button_pin_actions(self) -> list:
        return self.actions


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


class Action(ABC):
    """Represents a single action"""

    def __init__(self,
                 trigger: ActionTrigger,
                 action_type: ActionType,
                 delay: int,
                 output_pins: list,
                 notification: Notification,
                 condition: Condition):
        self.trigger = trigger
        self.action_type = action_type
        self.delay = delay
        all(isinstance(el, OutputPin) for el in output_pins)
        self.output_pins = output_pins
        self.notification = notification
        self.condition = condition

    def should_trigger(self, value: bool):
        return self.trigger.should_trigger(value)

    @abstractmethod
    def perform_action(self, pins_to_switch_on: {}, pins_to_switch_off: {}):
        pass

    def check_condition(self):
        if self.condition is None:
            return True
        return self.condition.verify()


class OnAction(Action):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 output_pins: list,
                 notification: Notification,
                 condition: Condition):
        super(OnAction, self).__init__(trigger, ActionType.ON, delay, output_pins, notification, condition)

    def perform_action(self, pins_to_switch_on: {}, pins_to_switch_off: {}):
        for pin in self.output_pins:
            logger.debug(f"pin number: '{pin.number}' with parent: '{pin.parent}'")
            pins_to_switch_on.setdefault(pin.parent, []).append(pin.number)
        logger.debug(f"Pins to switch on: '{pins_to_switch_on}'")


class OffAction(Action):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 output_pins: list,
                 notification: Notification,
                 condition: Condition):
        super(OffAction, self).__init__(trigger, ActionType.OFF, delay, output_pins, notification, condition)

    def perform_action(self, pins_to_switch_on: {}, pins_to_switch_off: {}):
        for pin in self.output_pins:
            pins_to_switch_off.setdefault(pin.parent, []).append(pin.number)


class ToggleAction(Action):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 output_pins: list,
                 notification: Notification,
                 master: OutputPin,
                 condition: Condition):
        super(ToggleAction, self).__init__(trigger, ActionType.TOGGLE, delay, output_pins, notification, condition)
        self.master = master

    def perform_action(self, pins_to_switch_on: {}, pins_to_switch_off: {}):
        # if master is on put all the lights of and visa versa
        if self.master.state:
            for pin in self.output_pins:
                pins_to_switch_off.setdefault(pin.parent, []).append(pin.number)
        else:
            for pin in self.output_pins:
                pins_to_switch_on.setdefault(pin.parent, []).append(pin.number)


class Arduino:
    """Represents an actual arduino"""

    def __init__(self, name: str, number_of_outputs_pins: int, number_of_button_pins: int):
        self.name = name
        self.number_of_output_pins = number_of_outputs_pins
        self.number_of_button_pins = number_of_button_pins
        self.output_pins = {}
        self.button_pins = {}

    def set_relay_pins(self, relay_pins: list):
        # Check that all elements in our list are actual OutputPin objects
        # This check is completely unnecessary, but gives us some assurances
        all(isinstance(el, OutputPin) for el in relay_pins)
        for pin in relay_pins:
            self.output_pins[pin.number] = pin

    def set_button_pins(self, button_pins: list):
        # Check that all elements in our list are actual button_pins objects
        all(isinstance(el, ButtonPin) for el in button_pins)
        for pin in button_pins:
            self.button_pins[pin.number] = pin

    def get_relay_status(self) -> str:
        """Gets the status array of the relay_pins of this arduino"""
        # Initialize empty state array
        pin_states = [0] * self.number_of_output_pins
        # Loop over all relay_pins and set their state in the array
        for pin in self.output_pins.values():
            pin_states[pin.number] = 1 if pin.state else 0

        # convert array to hex string
        return util.convert_array_to_hex(pin_states)

    def set_relay_status(self, payload: str):
        status = util.convert_hex_to_array(payload, self.number_of_output_pins)
        for pin in self.output_pins.values():
            if int(status[pin.number]) == 1:
                pin.state = True
            else:
                pin.state = False

    def get_changed_pins(self, payload: str) -> {}:
        status = util.convert_hex_to_array(payload, self.number_of_output_pins)
        changed_pins = {}
        for pin in self.button_pins.values():
            if bool(int(status[pin.number])) != pin.state:
                changed_pins[pin.number] = bool(int(status[pin.number]))
                pin.state = bool(int(status[pin.number]))
        return changed_pins


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


class Operator(Enum):
    AND = 1
    OR = 2


class Condition(ABC):
    @abstractmethod
    def verify(self) -> bool:
        pass


class ConditionList(Condition):
    def __init__(self, operator: Operator, conditions: list):
        self.operator = operator
        all(isinstance(el, Condition) for el in conditions)
        self.conditions = conditions

    def verify(self) -> bool:
        if self.operator == Operator.AND:
            for condition in self.conditions:
                if not condition.verify():
                    return False
            return True
        # Otherwise it's OR
        for condition in self.conditions:
            if condition.verify():
                return True
            return False


class OutputPinCondition(Condition):
    def verify(self) -> bool:
        NotImplementedError
        pass


class TimeCondition(Condition):
    def verify(self) -> bool:
        NotImplementedError
        pass
