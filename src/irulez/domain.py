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


class Condition(ABC):
    def __init__(self, condition_type: ConditionType):
        self.condition_type = condition_type


class Notification(ABC):
    def __init__(self, message: str, enabled: False):
        self.message = message
        self.enabled = enabled

    @abstractmethod
    def get_topic_name(self):
        pass

    @abstractmethod
    def get_payload(self):
        pass


class ImmediatelyActionTrigger(ActionTrigger):
    def __init__(self):
        super(ImmediatelyActionTrigger, self).__init__(ActionTriggerType.IMMEDIATELY)


class AfterReleaseActionTrigger(ActionTrigger):
    def __init__(self):
        super(AfterReleaseActionTrigger, self).__init__(ActionTriggerType.AFTER_RELEASE)


class LongDownActionTrigger(ActionTrigger):
    def __init__(self, seconds_down: int):
        super(LongDownActionTrigger, self).__init__(ActionTriggerType.LONG_DOWN)
        self._seconds_down = seconds_down

    @property
    def seconds_down(self):
        return self._seconds_down


class DoubleTapActionTrigger(ActionTrigger):
    def __init__(self, time_between_tap: int):
        super(DoubleTapActionTrigger, self).__init__(ActionTriggerType.DOUBLE_TAP)
        self.time_between_tap = time_between_tap


class TripleTapActionTrigger(ActionTrigger):
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


class IndividualAction:
    """Represents the actions on pins that have to happen on a single arduino"""
    def __init__(self,
                 delay: int,
                 pin_numbers_on: List[int],
                 pin_numbers_off: List[int]):
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


class Action(ABC):
    """Represents a single action"""

    def __init__(self,
                 trigger: ActionTrigger,
                 action_type: ActionType,
                 delay: int,
                 output_pins: List[OutputPin],
                 notifications: List[Notification],
                 condition: Optional[Condition]):
        self.trigger = trigger
        self.action_type = action_type
        self.delay = delay
        self.output_pins = output_pins
        self.notifications = notifications
        self.condition = condition

    @abstractmethod
    def perform_action(self, pins_to_switch: Dict[str, List[IndividualAction]]):
        pass

    def get_condition(self) -> Condition:
        return self.condition


class ButtonPin(Pin):
    """Represents a single input pin on an arduino"""
    def __init__(self, number: int, actions: List[Action], state=False):
        super(ButtonPin, self).__init__(number, ArduinoPinType.BUTTON, state)
        self.__actions = actions
        self.__long_down_timer = None
        self.__longdown_executed = False

    def set_button_pin_actions(self, actions: List[Action]):
        self.__actions = actions

    def get_button_pin_actions(self) -> List[Action]:
        return self.__actions

    def get_button_immediate_actions(self) -> List[Action]:
        results = []
        for action in self.__actions:
            if action.trigger.trigger_type == ActionTriggerType.IMMEDIATELY:
                results.append(action)
        return results

    def get_button_after_release_actions(self) -> List[Action]:
        results = []
        for action in self.__actions:
            if action.trigger.trigger_type == ActionTriggerType.AFTER_RELEASE:
                results.append(action)
        return results

    def get_smallest_longdown_time(self, minimum_time: int) -> Optional[int]:
        longdown_time = None
        for action in self.__actions:
            if action.trigger.trigger_type == ActionTriggerType.LONG_DOWN:
                if longdown_time is None or (longdown_time > action.trigger.seconds_down > minimum_time):
                    longdown_time = action.trigger.seconds_down
        return longdown_time

    def get_button_long_down_actions(self, seconds_down: int) -> List[Action]:
        results = []
        for action in self.__actions:
            if action.trigger.trigger_type == ActionTriggerType.LONG_DOWN and \
                            action.trigger.seconds_down == seconds_down:
                results.append(action)
        return results

    def start_long_down_timer(self, time:int, function, args: List[object]):
        self.__long_down_timer = Timer(time, function, args=(args,))
        self.__long_down_timer.start()

    def stop_long_down_timer(self):
        self.__long_down_timer.cancel()
        self.__long_down_timer = None

    @property
    def long_down_timer(self) -> Timer:
        return self.__long_down_timer

    @long_down_timer.setter
    def long_down_timer(self, long_down_timer: Timer):
        self.__long_down_timer = long_down_timer

    @property
    def longdown_executed(self) -> bool:
        return self.__longdown_executed

    @longdown_executed.setter
    def longdown_executed(self, longdown_executed: bool):
        self.__longdown_executed = longdown_executed


class MailNotification(Notification):
    def __init__(self, message: str, subject: str, mails: List[str], enabled=False):
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
    def __init__(self, message: str, tokens: List[str], enabled=False):
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


class OutputPinCondition(Condition):
    def __init__(self, output_pin: OutputPin, status: bool):
        super(OutputPinCondition, self).__init__(ConditionType.OUTPUT_PIN)
        self.output_pin = output_pin
        self.status = status


class TimeCondition(Condition):
    def __init__(self, from_time: time, to_time: time):
        super(TimeCondition, self).__init__(ConditionType.TIME)
        self.from_time = from_time
        self.to_time = to_time


class OnAction(Action):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 off_timer: int,
                 output_pins: List[OutputPin],
                 notifications: List[Notification],
                 condition: Optional[Condition]):
        self.off_timer = off_timer
        super(OnAction, self).__init__(trigger, ActionType.ON, delay, output_pins, notifications, condition)

    def perform_action(self, pins_to_switch: Dict[str, List[IndividualAction]]):
        pin_action = IndividualAction(self.delay, [], [])
        for pin in self.output_pins:
            logger.debug(f"pin number: '{pin.number}' with parent: '{pin.parent}'")
            pin_action.add_pin_on(pin.number)
        if pin_action.has_values_on():
            pins_to_switch.setdefault(pin.parent, []).append(pin_action)
        logger.debug(f"Pins to switch on: '{str(pin_action.pin_numbers_on)}'")

        if self.off_timer > 0:
            pin_action = IndividualAction(self.delay, [], [])
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
                 notifications: List[Notification],
                 condition: Optional[Condition]):
        self.on_timer = on_timer
        super(OffAction, self).__init__(trigger, ActionType.OFF, delay, output_pins, notifications, condition)

    def perform_action(self, pins_to_switch: Dict[str, List[IndividualAction]]):
        pin_action = IndividualAction(self.delay, [], [])
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
                 notifications: List[Notification],
                 master: OutputPin,
                 condition: Optional[Condition]):
        super(ToggleAction, self).__init__(trigger, ActionType.TOGGLE, delay, output_pins, notifications, condition)
        self.master = master

    def perform_action(self, pins_to_switch: Dict[str, List[IndividualAction]]):
        # if master is on put all the lights of and visa versa
        pin_action = IndividualAction(self.delay, [], [])
        if self.master.state:
            for pin in self.output_pins:
                pin_action.add_pin_off(pin.number)
            if pin_action.has_values_off():
                pins_to_switch.setdefault(pin.parent, []).append(pin_action)
            logger.debug(f"Pins to switch off: '{str(pin_action.pin_numbers_off)}'")
        else:
            for pin in self.output_pins:
                pin_action.add_pin_on(pin.number)
            if pin_action.has_values_on():
                pins_to_switch.setdefault(pin.parent, []).append(pin_action)
            logger.debug(f"Pins to switch on: '{str(pin_action.pin_numbers_on)}'")


class Arduino:
    """Represents an actual arduino"""

    def __init__(self, name: str, number_of_outputs_pins: int, number_of_button_pins: int):
        self.name = name
        self.number_of_output_pins = number_of_outputs_pins
        self.number_of_button_pins = number_of_button_pins
        self.output_pins = dict()
        self._button_pins = dict()

    @property
    def button_pins(self) -> Dict[int, ButtonPin]:
        return self._button_pins

    def set_output_pin(self, output_pin: OutputPin):
        self.output_pins[output_pin.number] = output_pin

    def set_output_pins(self, output_pins: List[OutputPin]):
        for pin in output_pins:
            self.output_pins[pin.number] = pin

    def set_button_pin(self, button_pin: ButtonPin):
        self._button_pins[button_pin.number] = button_pin

    def set_button_pins(self, button_pins: List[ButtonPin]):
        for pin in button_pins:
            self._button_pins[pin.number] = pin

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
                pin.state = True
            else:
                pin.state = False

    def get_changed_pins(self, payload: str) -> Dict[int, bool]:
        status = util.convert_hex_to_array(payload, self.number_of_output_pins)
        changed_pins = dict()
        for pin in self._button_pins.values():
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
