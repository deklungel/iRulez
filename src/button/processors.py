import src.button.mqtt_sender as mqtt_sender
import src.irulez.log as log
import src.irulez.domain as domain
from typing import Dict, List
logger = log.get_logger('button_processor')


class ButtonActionProcessor:
    """
    Process a new state of a button

    If a button has Immediate triggers and LongDown triggers, the Immediate trigger will fire always on button_down
    If a button has AfterRelease triggers and LongDown triggers, only one type will be triggered
    """

    # if button_pressed
    #   if button has Immediate triggers
    #       fire Immediate actions
    #   if button has LongDown triggers
    #       start button.timer of smallest longdown trigger
    # else if button_unpressed
    #   if button.timer is running
    #       cancel timer
    #       if not button.longdown_executed
    #           execute AfterRelease
    #   else
    #       if not button.longdown_executed
    #           fire AfterRelease
    #   remove flag longdown_executed
    # else if button.timer fired
    #   if button.timer is not running
    #       return
    #   execute LongDown with time passed (don't fire with smaller triggers)
    #   set flag longdown_executed
    #   if button has LongDown with larger triggers
    #       start new button.timer (remember time already passed)
    def __init__(self, sender: mqtt_sender.MqttSender, arduinos: {}):
        self.sender = sender
        self.arduinos = arduinos

    def execute_action(self, action: domain.Action, pins_to_switch: Dict[str, List[domain.IndividualAction]]):
        if action.check_condition():
            logger.info(f"Process action with type '{action.action_type}'")
            action.perform_action(pins_to_switch)
            self.process_notification(action)
        else:
            logger.info(f"Condition not met")

    def button_pressed(self, button: domain.ButtonPin):
        #   if button has Immediate triggers
        #       fire Immediate actions
        #   if button has LongDown triggers
        #       start button.timer of smallest longdown trigger
        pins_to_switch = {}
        for action in button.get_button_immediate_actions():
            self.execute_action(action, pins_to_switch)
        self.sender.publish_relative_action(pins_to_switch)

    def button_unpressed(self, button: domain.ButtonPin):
        #   if button.timer is running
        #       cancel timer
        #       if not button.longdown_executed
        #           execute AfterRelease
        #   else
        #       if not button.longdown_executed
        #           fire AfterRelease
        #   remove flag longdown_executed
        pass

    def button_timer_fired(self, button: domain.ButtonPin, seconds_down: int):
        #   if button.timer is not running
        #       return
        #   execute LongDown with time passed (don't fire with smaller triggers)
        #   set flag longdown_executed
        #   if button has LongDown with larger triggers
        #       start new button.timer (remember time already passed)
        pass

    def process_button(self, arduino: domain.Arduino, pin, value: bool):
        button = arduino.button_pins[pin]
        if value:
            self.button_pressed(button)
        else:
            self.button_unpressed(button)

    def process_notification(self, action: domain.Action):
        if action.notifications is None:
            return
        for notification in action.notifications:
            topic = notification.get_topic_name()
            payload = notification.get_payload()
            self.sender.publish_notification(topic, payload)

    def process_button_message(self, name: str, payload: str):
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return
        logger.debug("find changed pins")
        changed_pins = arduino.get_changed_pins(payload)
        logger.debug(f"changed pins found '{changed_pins}'")
        for pin, value in changed_pins.items():
            self.process_button(arduino, pin, value)


class RelayStatusProcessor:
    def __init__(self, arduinos: {}):
        self.arduinos = arduinos

    def update_arduino_output_pins(self, name: str, payload: str):
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return
        logger.debug(f"Board with name '{name}' found")
        arduino.set_output_pin_status(payload)
        logger.debug(f"relay status HEX: '{arduino.get_output_pin_status()}'.")
