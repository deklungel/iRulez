from enum import IntEnum
import src.irulez.util as util
from abc import ABC, abstractmethod
import src.irulez.log as log
from datetime import datetime, time
from typing import List, Dict, Optional
import src.irulez.constants as constants
import json

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
    def __init__(self,message: str, enabled: False):
        self.message = message
        self.enabled = enabled

    @abstractmethod
    def get_topic_name(self):
        pass

    @abstractmethod
    def get_payload(self):
        pass


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
                 notifications: Optional[List[Notification]],
                 condition: Optional[Condition]):
        self.trigger = trigger
        self.action_type = action_type
        self.delay = delay
        self.output_pins = output_pins
        self.notifications = notifications
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

    def __init__(self, number: int, actions: List[Action],down_timer, state=False):
        super(ButtonPin, self).__init__(number, ArduinoPinType.BUTTON, state)
        self.actions = actions
        self.down_timer = down_timer

    def set_button_pin_actions(self, actions: List[Action]):
        self.actions = actions

    def get_button_pin_actions(self) -> List[Action]:
        return self.actions


class MailNotification(Notification):
    def __init__(self,message: str, subject: str, mails: List[str], enabled=False):
        super(MailNotification, self).__init__(message, enabled)
        self.mails = mails
        self.subject = subject

    def get_topic_name(self):
        return constants.arduinoTopic + "/" + constants.notificationTopic + "/" + constants.mailTopic

    def get_payload(self):
        return json.dumps(
            {
                "mails": self.mails,
                "message": self.message,
                "subject": self.subject
            })


class TelegramNotification(Notification):
    def __init__(self,message:str, tokens: List[str], enabled=False):
        super(TelegramNotification, self).__init__(message, enabled)
        self.tokens = tokens

    def get_topic_name(self):
        return constants.arduinoTopic + "/" + constants.notificationTopic + "/" + constants.telegramTopic

    def get_payload(self):
        return json.dumps(
                    {
                        "tokens": self.tokens,
                        "message": self.message
                    })

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
    def __init__(self, name: str, topic: str, delay: int, pin_numbers_on: List[int], pin_numbers_off: List[int]):
        self.name = name
        self.topic = topic
        self.delay = delay
        self.pin_numbers_on = pin_numbers_on
        self.pin_numbers_off = pin_numbers_off

    def add_pin_on(self, pin_number: int):
        self.pin_numbers_on.append(pin_number)

    def add_pin_off(self, pin_number: int):
        self.pin_numbers_off.append(pin_number)

    def has_values_on(self) -> bool:
        if len(self.pin_numbers_on) > 0:
            return True
        return False

    def has_values_off(self) -> bool:
        if len(self.pin_numbers_off) > 0:
            return True
        return False


class OnAction(Action):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 off_timer: int,
                 output_pins: List[OutputPin],
                 notifications: Optional[Notification],
                 condition: Optional[Condition]):
        self.off_timer = off_timer
        super(OnAction, self).__init__(trigger, ActionType.ON, delay, output_pins, notifications, condition)

    def perform_action(self, pins_to_switch: Dict[str, List[IndividualAction]]):
        pin_action = IndividualAction(None, None, self.delay, [], [])
        for pin in self.output_pins:
            logger.debug(f"pin number: '{pin.number}' with parent: '{pin.parent}'")
            pin_action.add_pin_on(pin.number)
        if pin_action.has_values_on():
            pins_to_switch.setdefault(pin.parent, []).append(pin_action)
        logger.debug(f"Pins to switch on: '{str(pinAction.pin_numbers_on)}'")

        if self.off_timer > 0:
            pin_action = IndividualAction(None, None, self.delay, [], [])
            for pin in self.output_pins:
                pin_action.add_pin_off(pin.number)
            if pin_action.has_values_off():
                pins_to_switch.setdefault(pin.parent, []).append(pin_action)


class OffAction(Action):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 on_timer: int,
                 output_pins: List[OutputPin],
                 notifications: Optional[Notification],
                 condition: Optional[Condition]):
        self.on_timer = on_timer
        super(OffAction, self).__init__(trigger, ActionType.OFF, delay, output_pins, notifications, condition)

    def perform_action(self, pins_to_switch: Dict[str, List[IndividualAction]]):
        pin_action = IndividualAction(None, None, self.delay, [], [])
        for pin in self.output_pins:
            pin_action.add_pin_off(pin.number)
        if pin_action.has_values_off():
            pins_to_switch.setdefault(pin.parent, []).append(pin_action)

        if self.on_timer > 0:
            pin_action = IndividualAction(self.on_timer, [], [])
            for pin in self.output_pins:
                pin_action.add_pin_on(pin.number)
            if pin_action.has_values_on():
                pins_to_switch.setdefault(pin.parent, []).append(pin_action)


class ToggleAction(Action):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 output_pins: List[OutputPin],
                 notifications: Optional[Notification],
                 master: OutputPin,
                 condition: Optional[Condition]):
        super(ToggleAction, self).__init__(trigger, ActionType.TOGGLE, delay, output_pins, notifications, condition)
        self.master = master

    def perform_action(self, pins_to_switch: Dict[str, IndividualAction]):
        # if master is on put all the lights of and visa versa
        pinAction = IndividualAction(None, None, self.delay, [], [])
        if self.master.state:
            for pin in self.output_pins:
                pinAction.add_pin_off(pin.number)
            if pinAction.has_values_off():
                pins_to_switch.setdefault(pin.parent, []).append(pinAction)
            logger.debug(f"Pins to switch off: '{str(pinAction.pin_numbers_off)}'")
        else:
            for pin in self.output_pins:
                pinAction.add_pin_on(pin.number)
            if pinAction.has_values_on():
                pins_to_switch.setdefault(pin.parent, []).append(pinAction)
            logger.debug(f"Pins to switch on: '{str(pinAction.pin_numbers_on)}'")


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
