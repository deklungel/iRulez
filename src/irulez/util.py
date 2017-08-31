import src.irulez.constants as constants


def is_arduino_topic(topic: str) -> bool:
    return topic.startswith(constants.arduinoTopic)


def is_arduino_action_topic(topic: str) -> bool:
    """Checks if the given topic is an action topic for an arduino"""
    # Format arduino_number/action/something
    return is_arduino_topic(topic) and topic.contains('/' + constants.actionTopic + '/')


def get_arduino_name_from_topic(topic: str) -> str:
    if not(is_arduino_topic(topic)):
        return ''
    return topic[len(constants.arduinoTopic):topic.find('/')]
