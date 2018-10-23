import src.irulez.constants as constants
import src.irulez.log as log
from typing import Optional
from typing import List, Dict
import json

logger = log.get_logger('util')


def is_arduino_topic(topic: str) -> bool:
    """Checks if the given topic is a topic of an arduino"""
    if topic is None:
        return False
    return topic.startswith(constants.iRulezTopic)


def is_arduino_action_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and '/' + constants.actionTopic in topic


def is_arduino_relative_action_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and '/' + constants.actionTopic + '/' + constants.relativeTopic in topic


def is_arduino_timer_action_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format irulez_unique/action/relative/timer
    return is_arduino_topic(topic) and '/' + constants.actionTopic + '/' + constants.relativeTopic + '/' + \
        constants.timerTopic in topic


def is_arduino_button_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and '/' + constants.buttonTopic in topic


def is_arduino_button_fired_topic(topic: str) -> bool:
    """Checks if the given topic is a button fired topic for an arduino"""
    return is_arduino_topic(topic) and '/' + constants.buttonTimerFiredTopic in topic


def is_arduino_multiclick_fired_topic(topic: str) -> bool:
    """Checks if the given topic is a button fired topic for an arduino"""
    return is_arduino_topic(topic) and '/' + constants.buttonMulticlickFiredTopic in topic


def is_arduino_status_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and '/' + constants.statusTopic in topic


def is_arduino_dimmer_status_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and '/' + constants.dimmerStatusTopic in topic


def is_arduino_dimmer_timer_fired_topic_for_timer_module(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format irulez_unique/action/dimmerTimerFired/timer
    return is_arduino_topic(topic) and '/' + constants.actionTopic + '/' + constants.dimmerTimerFired + '/' + \
        constants.timerTopic in topic


def is_arduino_dimmer_timer_fired_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for a dimmer"""
    # Format irulez_unique/action/dimmerTimerFired
    return is_arduino_topic(topic) and '/' + constants.actionTopic + '/' + constants.dimmerTimerFired in topic


def is_arduino_dimmer_action_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for a dimmer"""
    # Format irulez_unique/action/dimmerTimerFired
    return is_arduino_topic(topic) and '/' + constants.actionTopic + '/' + constants.dimmerModuleTopic in topic


def is_arduino_dimmer_cancelled_topic(topic: str) -> bool:
    """Checks if the given topic is a cancelled topic for a dimmer"""
    # Format irulez_unique/dimmerCancelled/dimmerTimerFired
    return is_arduino_topic(topic) and '/' + constants.dimmerCancelled + '/' + constants.dimmerModuleTopic in topic


def get_arduino_name_from_topic(topic: str) -> Optional[str]:
    """Retrieves the name of the arduino from an arduino topic, or None if it couldn't be found"""
    if not (is_arduino_topic(topic)):
        return None
    return topic[len(constants.iRulezTopic + '/'):topic.find('/', len(constants.iRulezTopic + '/'))]


def get_arduino_dimmerpin_from_topic(topic: str, name: str) -> Optional[int]:
    """Retrieves the name of the arduino from an arduino topic, or None if it couldn't be found"""
    if not (is_arduino_topic(topic)):
        return None
    return int(topic[len(constants.iRulezTopic + '/' + name + '/'):
                     topic.find('/', len(constants.iRulezTopic + '/' + name + '/'))])


def convert_array_to_hex(status: list) -> str:
    binary = ''
    logger.debug("status " + str(status))
    for digit in status:
        binary += str(int(digit))
    logger.debug("hex: " + str(hex(int(binary, 2)))[2:])
    return str(hex(int(binary, 2)))[2:]


def convert_hex_to_array(payload: str, number_of_pins: int) -> list:
    if payload == '':
        logger.debug("empty payload")
        payload = "0"
    logger.debug("convert_hex_to_array " + bin(int(payload, 16))[2:].zfill(number_of_pins))
    return list(bin(int(payload, 16))[2:].zfill(number_of_pins))


def compare_lists(begin_status: List[bool], end_status: List[bool]) -> bool:
    return begin_status == end_status


def serialize_json(to_serialize: Dict):
    return json.dumps(to_serialize)


def deserialize_json(serialized: str):
    return json.loads(serialized)


def get_int_from_json_object(json_object, key: str) -> int:
    to_return = json_object[key]
    if to_return is None:
        return 0

    try:
        return int(to_return)
    except ValueError:
        logger.error(f"{to_return} could not be cast to an int.")

    return 0


def get_str_from_json_object(json_object, key: str) -> str:
    return json_object[key]


def get_int_list_from_json_object(json_object, key: str) -> List[int]:
    return json_object[key]


def get_bool_from_json_object(json_object, key: str) -> bool:
    to_return = json_object[key]
    if to_return is None:
        return False

    try:
        return bool(to_return)
    except ValueError:
        logger.error(f"{to_return} could not be cast to an int.")

    return False
