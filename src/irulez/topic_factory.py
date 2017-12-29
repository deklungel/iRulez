import src.irulez.constants as constants


def create_arduino_dimaction_topic(arduino_name: str, pin_number: int) -> str:
    """Topic used to send dimmer action messages to an arduino"""
    return constants.arduinoTopic + '/' + arduino_name + '/' + constants.dimAction + '/' + str(pin_number)


def create_timer_dimmer_timer_fired_topic() -> str:
    """Topic used to send a 'start dimmer timer' command to the timer module"""
    return constants.arduinoTopic + '/' + constants.actionTopic + '/' + \
        constants.dimmerTimerFired + '/' + constants.timerTopic


def create_timer_dimmer_timer_fired_response_topic() -> str:
    """Topic that will be used when a 'dimmer timer' command is executed by the timer module"""
    return constants.arduinoTopic + '/' + constants.actionTopic + '/' + constants.dimmerTimerFired