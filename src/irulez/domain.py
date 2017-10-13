from enum import IntEnum
import src.irulez.util as util
from abc import ABC, abstractmethod
import src.irulez.log as log
from datetime import datetime, time
from typing import List, Dict, Optional

logger = log.get_logger('domain')


class ArduinoPinType(IntEnum):
    """Represents the purpose of a pin on an arduino"""
    BUTTON = 1
    OUTPUT = 2
    DIMMER = 3


class ActionType(IntEnum):
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


class ActionTriggerType(IntEnum):
    """Represents when a action need to be executed"""
    IMMEDIATELY = 1
    AFTER_RELEASE = 2
    LONG_DOWN = 3
    DOUBLE_TAP = 4
    TRIPLE_TAP = 5


class Operator(IntEnum):
    AND = 1
    OR = 2


class ConditionType(IntEnum):
    LIST = 1
    OUTPUT_PIN = 2
    TIME = 3


class ActionTrigger(ABC):
    def __init__(self, trigger_type: ActionTriggerType):
        self.trigger_type = trigger_type

    def get_action_trigger_type(self):
        return self.trigger_type

    @abstractmethod
    def should_trigger(self, value: bool):
        pass


class Condition(ABC):
    def __init__(self, condition_type: ConditionType):
        self.condition_type = condition_type

    @abstractmethod
    def verify(self) -> bool:
        pass


class Notification(ABC):
    def __init__(self, enabled: False):
        self.enabled = enabled


class ImmediatelyActionTrigger(ActionTrigger):
    def should_trigger(self, value: bool):
        return value

    def __init__(self):
        super(ImmediatelyActionTrigger, self).__init__(ActionTriggerType.IMMEDIATELY)


class AfterReleaseActionTrigger(ActionTrigger):
    def should_trigger(self, value: bool):
        return not value

    def __init__(self):
        super(AfterReleaseActionTrigger, self).__init__(ActionTriggerType.AFTER_RELEASE)


class LongDownActionTrigger(ActionTrigger):
    def should_trigger(self, value: bool):
        NotImplementedError
        pass

    def __init__(self, seconds_down: int):
        super(LongDownActionTrigger, self).__init__(ActionTriggerType.LONG_DOWN)
        self.seconds_down = seconds_down


class DoubleTapActionTrigger(ActionTrigger):
    def should_trigger(self, value: bool):
        NotImplementedError
        pass

    def __init__(self, time_between_tap: int):
        super(DoubleTapActionTrigger, self).__init__(ActionTriggerType.DOUBLE_TAP)
        self.time_between_tap = time_between_tap


class TripleTapActionTrigger(ActionTrigger):
    def should_trigger(self, value: bool):
        NotImplementedError
        pass

    def __init__(self, time_between_tap: int):
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


class Action(ABC):
    """Represents a single action"""

    def __init__(self,
                 trigger: ActionTrigger,
                 action_type: ActionType,
                 delay: int,
                 output_pins: List[OutputPin],
                 notification: Optional[Notification],
                 condition: Optional[Condition]):
        self.trigger = trigger
        self.action_type = action_type
        self.delay = delay
        self.output_pins = output_pins
        self.notification = notification
        self.condition = condition

    def should_trigger(self, value: bool):
        return self.trigger.should_trigger(value)

    @abstractmethod
    def perform_action(self, pins_to_switch_on: Dict[str, List[int]], pins_to_switch_off: Dict[str, List[int]]):
        pass

    def check_condition(self):
        if self.condition is None:
            return True
        return self.condition.verify()


class ButtonPin(Pin):
    """Represents a single input pin on an arduino"""

    def __init__(self, number: int, actions: List[Action], state=False):
        super(ButtonPin, self).__init__(number, ArduinoPinType.BUTTON, state)
        self.actions = actions

    def set_button_pin_actions(self, actions: List[Action]):
        self.actions = actions

    def get_button_pin_actions(self) -> List[Action]:
        return self.actions


class MailNotification(Notification):
    def __init__(self, email: str, enabled=False):
        super(MailNotification, self).__init__(enabled)
        self.email = email


class TelegramNotification(Notification):
    def __init__(self, token: str, enabled=False):
        super(TelegramNotification, self).__init__(enabled)
        self.token = token


class ConditionList(Condition):
    def __init__(self, operator: Operator, conditions: List[Condition]):
        super(ConditionList, self).__init__(ConditionType.LIST)
        self.operator = operator
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
    def __init__(self, output_pin: OutputPin, status: bool):
        super(OutputPinCondition, self).__init__(ConditionType.OUTPUT_PIN)
        self.output_pin = output_pin
        self.status = status

    def verify(self) -> bool:
        return self.output_pin.state == self.status


class TimeCondition(Condition):
    def __init__(self, from_time: time, to_time: time):
        super(TimeCondition, self).__init__(ConditionType.TIME)
        self.from_time = from_time
        self.to_time = to_time

    def verify(self) -> bool:
        return self.from_time <= datetime.now().time() <= self.to_time

class IndividualAction:
    def __init__(self, delay: int, pinNumbers: []):
        self.delay = delay
        self.pinNumbers = pinNumbers

    def addpin(self, pinNumber: int):
        self.pinNumbers.append(pinNumber)

    def hasvalues(self) -> bool:
        if len(self.pinNumbers) > 0:
            return True
        return False

class OnAction(Action):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 output_pins: List[OutputPin],
                 notification: Optional[Notification],
                 condition: Optional[Condition]):
        super(OnAction, self).__init__(trigger, ActionType.ON, delay, output_pins, notification, condition)

    def perform_action(self, pins_to_switch_on: Dict[str, List[int]], pins_to_switch_off: Dict[str, List[int]]):
        pinAction = IndividualAction(self.delay, [])
        for pin in self.output_pins:
            logger.debug(f"pin number: '{pin.number}' with parent: '{pin.parent}'")
            pinAction.addpin(pin.number)
        if pinAction.hasvalues:
                pins_to_switch_on.setdefault(pin.parent, []).append(pinAction)
        logger.debug(f"Pins to switch on: '{str(pinAction.pinNumbers)}'")


class OffAction(Action):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 output_pins: List[OutputPin],
                 notification: Optional[Notification],
                 condition: Optional[Condition]):
        super(OffAction, self).__init__(trigger, ActionType.OFF, delay, output_pins, notification, condition)

    def perform_action(self, pins_to_switch_on: Dict[str, List[int]], pins_to_switch_off: Dict[str, List[int]]):
        pinAction = IndividualAction(self.delay, [])
        for pin in self.output_pins:
            pinAction.addpin(pin.number)
        if pinAction.hasvalues:
            pins_to_switch_off.setdefault(pin.parent, []).append(pinAction)


class ToggleAction(Action):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 output_pins: List[OutputPin],
                 notification: Optional[Notification],
                 master: OutputPin,
                 condition: Optional[Condition]):
        super(ToggleAction, self).__init__(trigger, ActionType.TOGGLE, delay, output_pins, notification, condition)
        self.master = master

    def perform_action(self, pins_to_switch_on: Dict[str, IndividualAction], pins_to_switch_off: Dict[str, IndividualAction]):
        # if master is on put all the lights of and visa versa
        pinAction = IndividualAction(self.delay,[])
        if self.master.state:
            for pin in self.output_pins:
                pinAction.addpin(pin.number)
            if pinAction.hasvalues:
                pins_to_switch_off.setdefault(pin.parent, []).append(pinAction)
            logger.debug(f"Pins to switch off: '{str(pinAction.pinNumbers)}'")
        else:
            for pin in self.output_pins:
                pinAction.addpin(pin.number)
            if pinAction.hasvalues:
                pins_to_switch_on.setdefault(pin.parent, []).append(pinAction)
            logger.debug(f"Pins to switch on: '{str(pinAction.pinNumbers)}'")




class Arduino:
    """Represents an actual arduino"""

    def __init__(self, name: str, number_of_outputs_pins: int, number_of_button_pins: int):
        self.name = name
        self.number_of_output_pins = number_of_outputs_pins
        self.number_of_button_pins = number_of_button_pins
        self.output_pins = dict()
        self.button_pins = dict()

    def set_output_pin(self, output_pin: OutputPin):
        self.output_pins[output_pin.number] = output_pin

    def set_output_pins(self, output_pins: List[OutputPin]):
        for pin in output_pins:
            self.output_pins[pin.number] = pin

    def set_button_pin(self, button_pin: ButtonPin):
        self.button_pins[button_pin.number] = button_pin

    def set_button_pins(self, button_pins: List[ButtonPin]):
        for pin in button_pins:
            self.button_pins[pin.number] = pin

    def get_output_pin_status(self) -> str:
        """Gets the status array of the output_pins of this arduino"""
        # Initialize empty state array
        pin_states = [0] * self.number_of_output_pins
        # Loop over all output_pins and set their state in the array
        for pin in self.output_pins.values():
            pin_states[pin.number] = 1 if pin.state else 0

        # convert array to hex string
        return util.convert_array_to_hex(pin_states)

    def get_output_pin(self, pinNumber: int) -> OutputPin:
        return self.output_pins[pinNumber]

    def set_output_pin_status(self, payload: str):
        status = util.convert_hex_to_array(payload, self.number_of_output_pins)
        for pin in self.output_pins.values():
            if int(status[pin.number]) == 1:
                pin.state = True
            else:
                pin.state = False

    def get_changed_pins(self, payload: str) -> Dict[int, bool]:
        status = util.convert_hex_to_array(payload, self.number_of_output_pins)
        changed_pins = dict()
        for pin in self.button_pins.values():
            if bool(int(status[pin.number])) != pin.state:
                changed_pins[pin.number] = bool(int(status[pin.number]))
                pin.state = bool(int(status[pin.number]))
        return changed_pins


class ArduinoConfig:
    """Represents the configuration of all known arduinos"""

    def __init__(self, arduinos: List[Arduino]):
        self.arduinos = arduinos


class MqttConfig:
    """Represents the configuration of the mqtt service"""

    def __init__(self, address: str, port: int, username: str, password: str):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
