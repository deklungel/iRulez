import src.irulez.constants as constants
import src.irulez.log as log
from typing import Optional

logger = log.get_logger('util')


def is_arduino_topic(topic: str) -> bool:
    """Checks if the given topic is a topic of an arduino"""
    if topic is None:
        return False
    return topic.startswith(constants.arduinoTopic)


def is_arduino_action_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and '/' + constants.actionTopic in topic

def is_arduino_relative_action_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and '/' + constants.actionTopic + '/' + constants.relative in topic

def is_arduino_timer_action_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and '/' + constants.actionTopic + '/' + constants.relative + '/' + constants.timer in topic


def is_arduino_button_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and '/' + constants.buttonTopic in topic


def is_arduino_status_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and '/' + constants.statusTopic in topic


def get_arduino_name_from_topic(topic: str) -> Optional[str]:
    """Retrieves the name of the arduino from an arduino topic, or None if it couldn't be found"""
    if not(is_arduino_topic(topic)):
        return None
    return topic[len(constants.arduinoTopic + '/'):topic.find('/', len(constants.arduinoTopic + '/'))]


def convert_array_to_hex(status: list) -> str:
    binary = ''
    logger.debug("status " + str(status))
    for digit in status:
        binary += str(int(digit))
    logger.debug("hex " + str(hex(int(binary, 2)))[2:])
    return str(hex(int(binary, 2)))[2:]


def convert_hex_to_array(payload: str, number_of_pins: int) -> list:
    if payload == '':
        logger.debug("empty payload")
        payload = "0"
    logger.debug("convert_hex_to_array " + bin(int(payload, 16))[2:].zfill(number_of_pins))
    return bin(int(payload, 16))[2:].zfill(number_of_pins)
