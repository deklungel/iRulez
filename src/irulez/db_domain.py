from datetime import time


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
    def __init__(self, id: int, number: int, action_ids: list):
        self.action_ids = action_ids
        self.number = number
        self.id = id


class Action:
    def __init__(self, id: int, action_type: int, trigger_id: int, delay: int, output_pin_ids: list, notification_id: int,
                 condition_id: int):
        self.id = id
        self.condition_id = condition_id
        self.notification_id = notification_id
        self.output_pin_ids = output_pin_ids
        self.delay = delay
        self.action_type = action_type
        self.trigger_id = trigger_id


class Trigger:
    def __init__(self, id: int, trigger_type: int, seconds_down: int, time_between_tap: int):
        self.id = id
        self.time_between_tap = time_between_tap
        self.seconds_down = seconds_down
        self.trigger_type = trigger_type


class Condition:
    def __init__(self, id: int, type: str, operator: int, condition_ids: list, output_pin_id: int, status: bool,
                 from_time: time, to_time: time):
        self.id = id
        self.type = type
        self.to_time = to_time
        self.from_time = from_time
        self.status = status
        self.output_pin_id = output_pin_id
        self.condition_ids = condition_ids
        self.operator = operator
