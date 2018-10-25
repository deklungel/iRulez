from datetime import time
from typing import List, Optional


class Arduino:
    def __init__(self, id: int, name: str, template_id: int):
        self.id = id
        self.name = name
        self.template_id = template_id


class Template:
    def __init__(self, id: int, name: str, nb_input_pins: int, nb_output_pins: int):
        self.id = id
        self.name = name
        self.nb_input_pins = nb_input_pins
        self.nb_output_pins = nb_output_pins


class OutputPin:
    def __init__(self, id: int, number: int, parent_id: int):
        self.parent_id = parent_id
        self.number = number
        self.id = id


class InputPin:
    def __init__(self, id: int, number: int, action_ids: List[int], parent_id: int, time_between_clicks: float):
        self.parent_id = parent_id
        self.action_ids = action_ids
        self.number = number
        self.time_between_clicks = time_between_clicks
        self.id = id


class Action:
    def __init__(self,
                 id: int,
                 action_type: int,
                 trigger_id: int,
                 notification_ids: List[int],
                 delay: int,
                 timer: int,
                 output_pin_ids: List[int],
                 condition_id: Optional[int],
                 master_id: Optional[int],
                 click_number: int,
                 dimmer_speed: Optional[int],
                 cancel_on_button_release: Optional[bool],
                 dimmer_light_value: Optional[int],
                 master_dimmer_id: Optional[int]):
        """
        Creates a new Action

        :param id: The identifier of this action
        :param action_type: The kind of action. See src.button.domain.ActionType class for possible values
        :param trigger_id: The identifier of the trigger of this action
        :param notification_ids: The identifiers of the notifications of this action. Can be empty.
        :param delay: The delay before this action should be executed.
        :param timer: The timer after which the action should be reverted. Only applies for ON/OFF actions
        :param output_pin_ids: The identifiers of the output pins affected by this action.
        :param condition_id: The (optional) identifier of the condition that should apply for this action.
        :param master_id: The master pin that should determine the TOGGLE action. This pin will be looked at when
                            determining whether it should toggle on or off
        :param click_number: Number of times that has to be clicked on multiclick action to activate
        :param dimmer_speed: How fast/slow the dimmer has to change light intensity
        :param cancel_on_button_release: If this is set to true, the dimmer will stop dimming as soon
                                            as the button is released
        :param dimmer_light_value: If set to -1, a dimmer will remember its last known value before switching off
                                    If set to a value, a dimmer will go to this value by default/not remember last value
        :param master_dimmer_id: The identifier of the dimmer whose last known value should be taken when switching
                                    the dimmer on.
        """
        # General properties
        self.__id = id
        self.__trigger_id = trigger_id
        self.__action_type = action_type
        self.__delay = delay
        self.__output_pin_ids = output_pin_ids
        self.__notification_ids = notification_ids
        self.__condition_id = condition_id
        self.__click_number = click_number

        # ON/OFF/ON_DIMMER/OFF_DIMMER action
        self.__timer = timer

        # TOGGLE/TOGGLE_DIMMER action
        self.__master_id = master_id

        # DIMMER
        self.__dimmer_speed = dimmer_speed
        self.__cancel_on_button_release = cancel_on_button_release

        # ON_DIMMER/TOGGLE_DIMMER action
        self.__dimmer_light_value = dimmer_light_value
        self.__master_dimmer_id = master_dimmer_id

    @property
    def id(self) -> int:
        return self.__id

    @property
    def trigger_id(self) -> int:
        return self.__trigger_id

    @property
    def action_type(self) -> int:
        return self.__action_type

    @property
    def notification_ids(self) -> List[int]:
        return self.__notification_ids

    @property
    def delay(self) -> int:
        return self.__delay

    @property
    def output_pin_ids(self) -> List[int]:
        return self.__output_pin_ids

    @property
    def timer(self) -> int:
        return self.__timer

    @property
    def condition_id(self) -> Optional[int]:
        return self.__condition_id

    @property
    def master_id(self) -> Optional[int]:
        return self.__master_id

    @property
    def click_number(self) -> int:
        return self.__click_number

    @property
    def dimmer_speed(self) -> Optional[int]:
        return self.__dimmer_speed

    @property
    def cancel_on_button_release(self) -> Optional[bool]:
        return self.__cancel_on_button_release

    @property
    def dimmer_light_value(self) -> Optional[int]:
        return self.__dimmer_light_value

    @property
    def master_dimmer_id(self) -> Optional[int]:
        return self.__master_dimmer_id


class Trigger:
    def __init__(self, id: int, trigger_type: int, seconds_down: Optional[int]):
        self.id = id
        self.trigger_type = trigger_type
        self.seconds_down = seconds_down


class Condition:
    def __init__(self, id: int, type: int, operator: Optional[int], condition_ids: Optional[List[int]],
                 output_pin_id: Optional[int], status: Optional[bool], from_time: Optional[time],
                 to_time: Optional[time]):
        self.id = id
        self.type = type
        self.to_time = to_time
        self.from_time = from_time
        self.status = status
        self.output_pin_id = output_pin_id
        self.condition_ids = condition_ids
        self.operator = operator


class Notification:
    def __init__(self, id: int, message: str, notification_type: int, enabled: bool, subject: Optional[str],
                 mail_address: List[str], tokens: List[str]):
        self.id = id
        self.notification_type = notification_type
        self.message = message
        self.enabled = enabled
        self.subject = subject
        self.emails = mail_address
        self.tokens = tokens
