from enum import IntEnum
import src.irulez.util as util
from abc import ABC, abstractmethod
import src.irulez.log as log
from datetime import time
from typing import List, Dict, Optional
import src.irulez.constants as constants
from threading import Timer

logger = log.get_logger('button_domain')


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
    ON_DIMMER = 5
    OFF_DIMMER = 6
    TOGGLE_DIMMER = 7
    DIMMER = 8


class ActionTriggerType(IntEnum):
    """Represents when a action need to be executed"""
    IMMEDIATELY = 1
    AFTER_RELEASE = 2
    LONG_DOWN = 3


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

    def get_action_trigger_type(self) -> ActionTriggerType:
        return self.trigger_type


class Condition(ABC):
    def __init__(self, condition_type: ConditionType):
        self.condition_type = condition_type


class Notification(ABC):
    def __init__(self, message: str, enabled: False):
        self.message = message
        self.enabled = enabled

    @abstractmethod
    def get_topic_name(self) -> str:
        pass

    @abstractmethod
    def get_payload(self) -> str:
        pass


class ImmediatelyActionTrigger(ActionTrigger):
    def __init__(self) -> None:
        super(ImmediatelyActionTrigger, self).__init__(ActionTriggerType.IMMEDIATELY)


class AfterReleaseActionTrigger(ActionTrigger):
    def __init__(self) -> None:
        super(AfterReleaseActionTrigger, self).__init__(ActionTriggerType.AFTER_RELEASE)


class LongDownActionTrigger(ActionTrigger):
    def __init__(self, seconds_down: int):
        super(LongDownActionTrigger, self).__init__(ActionTriggerType.LONG_DOWN)
        self._seconds_down = seconds_down

    @property
    def seconds_down(self) -> int:
        return self._seconds_down


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


class IndividualDimAction:
    """Represents a dimmer action for a single arduino"""

    def __init__(self,
                 dim_speed: int,
                 dim_light_value: int,
                 delay: int):
        self.__speed = dim_speed
        self.__dim_light_value = dim_light_value
        self.__delay = delay
        self.__pin_numbers = []

    def add_pin(self, pin_number: int):
        self.__pin_numbers.append(pin_number)

    def has_values(self) -> bool:
        if len(self.__pin_numbers) > 0:
            return True
        return False

    @property
    def speed(self) -> int:
        return self.__speed

    @property
    def dim_light_value(self) -> int:
        return self.__dim_light_value

    @property
    def delay(self) -> int:
        return self.__delay

    @property
    def pin_numbers(self) -> List[int]:
        return self.__pin_numbers


class Action(ABC):
    """Represents a single action"""

    def __init__(self,
                 trigger: ActionTrigger,
                 action_type: ActionType,
                 delay: int,
                 output_pins: List[OutputPin],
                 notifications: List[Notification],
                 condition: Optional[Condition],
                 click_number: int):
        self.trigger = trigger
        self.action_type = action_type
        self.delay = delay
        self.output_pins = output_pins
        self.notifications = notifications
        self.condition = condition
        self.click_number = click_number

    def get_condition(self) -> Condition:
        return self.condition


class DimmerAction(Action):
    """Represents a single dimmer action"""

    def __init__(self,
                 trigger: ActionTrigger,
                 action_type: ActionType,
                 delay: int,
                 output_pins: List[OutputPin],
                 notifications: List[Notification],
                 condition: Optional[Condition],
                 click_number: int,
                 dimmer_speed: int):
        super(DimmerAction, self).__init__(trigger, action_type, delay, output_pins, notifications, condition,
                                           click_number)
        self._dimmer_speed = dimmer_speed


class ButtonPin(Pin):
    """Represents a single input pin on an arduino"""

    def __init__(self, number: int, actions: List[Action], time_between_clicks, state=False):
        self.__actions = actions
        self.__long_down_timer = None
        self.__multi_click_timer = None
        self.__longdown_executed = False
        self.__time_between_clicks = time_between_clicks
        self.__clicks = 0
        self.__dimmer_direction = True
        super(ButtonPin, self).__init__(number, ArduinoPinType.BUTTON, state)

    def get_button_immediate_actions(self) -> List[Action]:
        results = []
        for action in self.actions:
            if action.trigger.trigger_type == ActionTriggerType.IMMEDIATELY and self.clicks == action.click_number:
                results.append(action)
        return results

    def get_button_after_release_actions(self) -> List[Action]:
        results = []
        for action in self.actions:
            if action.trigger.trigger_type == ActionTriggerType.AFTER_RELEASE and self.clicks == action.click_number:
                results.append(action)
        return results

    def get_smallest_longdown_time(self, minimum_time: int) -> Optional[int]:
        longdown_time = None
        for action in self.actions:
            if action.click_number == self.clicks and action.trigger.trigger_type == ActionTriggerType.LONG_DOWN and \
                    isinstance(action.trigger, LongDownActionTrigger):
                if longdown_time is None and action.trigger.seconds_down > minimum_time:
                    longdown_time = action.trigger.seconds_down
                elif action.trigger.seconds_down > minimum_time:
                    longdown_time = action.trigger.seconds_down
        return longdown_time

    def get_button_long_down_actions(self, seconds_down: int) -> List[Action]:
        results = []
        for action in self.actions:
            if action.trigger.trigger_type == ActionTriggerType.LONG_DOWN and \
                    action.trigger.seconds_down == seconds_down and isinstance(action.trigger, LongDownActionTrigger):
                results.append(action)
        return results

    def has_multi_click_actions(self, minimum_click: int) -> bool:
        for action in self.actions:
            if minimum_click <= action.click_number > 1:
                return True
        return False

    def start_long_down_timer(self, interval: int, function, args: List[object]):
        logger.debug(f"Start long down timer")
        self.__long_down_timer = Timer(interval, function, args=(args,))
        self.__long_down_timer.start()

    def stop_long_down_timer(self) -> None:
        logger.debug(f"Stop long down timer")
        self.__long_down_timer.cancel()
        self.__long_down_timer = None

    def start_multi_click_timer(self, interval: int, function, args: List[object]):
        logger.debug(f"Start multi click timer")
        self.__multi_click_timer = Timer(interval, function, args=(args,))
        self.__multi_click_timer.start()

    def stop_multi_click_timer(self) -> None:
        logger.debug(f"Stop multi click timer")
        self.__multi_click_timer.cancel()
        self.__multi_click_timer = None

    def reverse_dimmer_direction(self) -> None:
        self.__dimmer_direction = not self.dimmer_direction

    @property
    def multi_click_timer(self) -> Timer:
        return self.__multi_click_timer

    @property
    def dimmer_direction(self) -> bool:
        return self.__dimmer_direction

    @dimmer_direction.setter
    def dimmer_direction(self, dimmer_direction: bool):
        self.__dimmer_direction = dimmer_direction

    @property
    def time_between_clicks(self) -> float:
        return self.__time_between_clicks

    @property
    def long_down_timer(self) -> Timer:
        return self.__long_down_timer

    @long_down_timer.setter
    def long_down_timer(self, long_down_timer: Timer):
        self.__long_down_timer = long_down_timer

    @property
    def clicks(self) -> int:
        return self.__clicks

    @clicks.setter
    def clicks(self, clicks: int):
        self.__clicks = clicks

    @property
    def actions(self) -> List[Action]:
        return self.__actions

    @property
    def longdown_executed(self) -> bool:
        return self.__longdown_executed

    @longdown_executed.setter
    def longdown_executed(self, longdown_executed: bool):
        self.__longdown_executed = longdown_executed


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

    def get_output_pin(self, pin_number: int) -> OutputPin:
        return self.output_pins[pin_number]

    def get_changed_pins(self, payload: str) -> Dict[int, bool]:
        status = util.convert_hex_to_array(payload, self.number_of_output_pins)
        changed_pins = dict()
        for pin in self._button_pins.values():
            if bool(int(status[pin.number])) != pin.state:
                changed_pins[pin.number] = bool(int(status[pin.number]))
                pin.state = bool(int(status[pin.number]))
        return changed_pins


class IndividualRealTimeDimAction(IndividualAction):
    """Represents a dimmer action for a single arduino"""

    def __init__(self,
                 dim_speed: int,
                 dim_light_value: int,
                 delay: int,
                 pin_numbers_on: List[int],
                 pin_numbers_off: List[int],
                 arduino: Arduino,
                 button: ButtonPin):
        super(IndividualAction).__init__(delay, pin_numbers_on, pin_numbers_off)
        self.speed = dim_speed
        self.dim_light_value = dim_light_value
        self.arduino = arduino
        self.button = button


class MailNotification(Notification):
    def __init__(self, message: str, subject: str, mails: List[str], enabled=False):
        super(MailNotification, self).__init__(message, enabled)
        self.mails = mails
        self.subject = subject

    def get_topic_name(self) -> str:
        return constants.arduinoTopic + "/" + constants.notificationTopic + "/" + constants.mailTopic

    def get_payload(self) -> str:
        return util.serialize_json(
            {
                "mails": self.mails,
                "message": self.message,
                "subject": self.subject
            })


class TelegramNotification(Notification):
    def __init__(self, message: str, tokens: List[str], enabled=False):
        super(TelegramNotification, self).__init__(message, enabled)
        self.tokens = tokens

    def get_topic_name(self) -> str:
        return constants.arduinoTopic + "/" + constants.notificationTopic + "/" + constants.telegramTopic

    def get_payload(self) -> str:
        return util.serialize_json(
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
                 condition: Optional[Condition],
                 click_number: int):
        self.off_timer = off_timer
        super(OnAction, self).__init__(trigger, ActionType.ON, delay, output_pins, notifications,
                                       condition, click_number)

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
                 condition: Optional[Condition],
                 click_number: int):
        self.on_timer = on_timer
        super(OffAction, self).__init__(trigger, ActionType.OFF, delay, output_pins, notifications,
                                        condition, click_number)

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
                 condition: Optional[Condition],
                 click_number: int):
        super(ToggleAction, self).__init__(trigger, ActionType.TOGGLE, delay, output_pins, notifications,
                                           condition, click_number)
        self.master = master

    def perform_action(self, pins_to_switch: Dict[str, List[IndividualAction]], master: bool):
        # if master is on put all the lights of and visa versa
        pin_action = IndividualAction(self.delay, [], [])
        if master:
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


class OnDimmerAction(DimmerAction):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 off_timer: int,
                 output_pins: List[OutputPin],
                 notifications: List[Notification],
                 condition: Optional[Condition],
                 click_number: int,
                 dimmer_speed: int,
                 dimmer_light_value: int):
        self.__off_timer = off_timer
        self.__dimmer_light_value = dimmer_light_value
        super(OnDimmerAction, self).__init__(trigger, ActionType.ON_DIMMER, delay, output_pins, notifications,
                                             condition, click_number, dimmer_speed)

    def perform_action(self, pin_to_dim: Dict[str, List[IndividualDimAction]]):
        pin_action = IndividualDimAction(self._dimmer_speed, self.__dimmer_light_value, self.delay)
        for pin in self.output_pins:
            logger.debug(f"pin number: '{pin.number}' with parent: '{pin.parent}'")
            pin_action.add_pin(pin.number)
            if pin_action.has_values():
                pin_to_dim.setdefault(pin.parent, []).append(pin_action)
        logger.debug(f"Pins to switch on: '{str(pin_action.pin_numbers_on)}'")

        if self.__off_timer > 0:
            pin_action = IndividualDimAction(self._dimmer_speed, 0, self.__off_timer)
            for pin in self.output_pins:
                pin_action.add_pin(pin.number)
                if pin_action.has_values():
                    pin_to_dim.setdefault(pin.parent, []).append(pin_action)


class OffDimmerAction(DimmerAction):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 on_timer: int,
                 output_pins: List[OutputPin],
                 notifications: List[Notification],
                 condition: Optional[Condition],
                 click_number: int,
                 dimmer_speed: int):
        self.__on_timer = on_timer
        super(OffDimmerAction, self).__init__(trigger, ActionType.OFF_DIMMER, delay, output_pins, notifications,
                                              condition, click_number, dimmer_speed)

    def perform_action(self, pin_to_dim: Dict[str, List[IndividualDimAction]]):
        pin_action = IndividualDimAction(self._dimmer_speed, 0, self.delay)
        for pin in self.output_pins:
            pin_action.add_pin(pin.number)
            if pin_action.has_values():
                pin_to_dim.setdefault(pin.parent, []).append(pin_action)

        if self.__on_timer > 0:
            pin_action = IndividualDimAction(self._dimmer_speed, 0, self.__on_timer)
            for pin in self.output_pins:
                pin_action.add_pin(pin.number)
                if pin_action.has_values():
                    pin_to_dim.setdefault(pin.parent, []).append(pin_action)


class ToggleDimmerAction(DimmerAction):
    def __init__(self,
                 trigger: ActionTrigger,
                 delay: int,
                 output_pins: List[OutputPin],
                 notifications: List[Notification],
                 master: OutputPin,
                 condition: Optional[Condition],
                 click_number: int,
                 dimmer_speed: int,
                 dimmer_light_value: int
                 ):
        super(ToggleDimmerAction, self).__init__(trigger, ActionType.TOGGLE_DIMMER, delay, output_pins, notifications,
                                                 condition, click_number, dimmer_speed)
        self.master = master
        self.__dimmer_light_value = dimmer_light_value

    def perform_action(self, pin_to_dim: Dict[str, List[IndividualDimAction]], master: int):
        # if master is on put all the lights of and visa versa
        if master > 0:
            pin_action = IndividualDimAction(self._dimmer_speed, 0, self.delay)
            for pin in self.output_pins:
                pin_action.add_pin(pin.number)
                if pin_action.has_values():
                    pin_to_dim.setdefault(pin.parent, []).append(pin_action)
            logger.debug(f"Pins to switch off: '{str(pin_action.pin_numbers_off)}'")
        else:
            pin_action = IndividualDimAction(self._dimmer_speed, self.__dimmer_light_value, self.delay)
            for pin in self.output_pins:
                pin_action.add_pin(pin.number)
                if pin_action.has_values():
                    pin_to_dim.setdefault(pin.parent, []).append(pin_action)
            logger.debug(f"Pins to switch on: '{str(pin_action.pin_numbers_on)}'")


# class DimAction(DimmerAction):
#
#     def __init__(self,
#                  trigger: ActionTrigger,
#                  delay: int,
#                  output_pins: List[OutputPin],
#                  notifications: List[Notification],
#                  master: OutputPin,
#                  condition: Optional[Condition],
#                  click_number: int,
#                  dimmer_speed: int,
#                  dimmer_light_value: int
#                  ):
#         super(DimAction, self).__init__(trigger, ActionType.DIMMER, delay, output_pins, notifications,
#                                         condition, click_number, dimmer_speed, dimmer_light_value)
#         self.master = master
#
#     def perform_action(self, pins_to_switch: Dict[str, List[IndividualAction]],
#                        pins_to_dim: Dict[str, List[IndividualDimAction]],
#                        pins_for_real_time_dimmer: Dict[str, List[IndividualRealTimeDimAction]],
#                        master, button: ButtonPin, arduino: Arduino):
#         # if master is on put all the lights of and visa versa
#         pin_action = IndividualRealTimeDimAction(self.dimmer_speed, self.dimmer_light_value, self.delay, [], [],
#                                                  arduino, button)


class ArduinoConfig:
    """Represents the configuration of all known arduinos"""

    def __init__(self, arduinos: List[Arduino]):
        self.arduinos = arduinos
