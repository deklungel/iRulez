import json
from datetime import datetime
from typing import Dict
import src.button.domain as domain
import src.button.mqtt_sender as mqtt_sender
import src.irulez.log as log
import src.output_status.ServiceClient as ServiceClient

logger = log.get_logger('button_processor')


class ButtonActionProcessor:
    """
    Process a new state of a button

    If a button has Immediate triggers and LongDown triggers, the Immediate trigger will fire always on button_down
    If a button has AfterRelease triggers and LongDown triggers, only one type will be triggered
    If a button has Immediate triggers and multiclick triggers
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


    def __init__(self, sender: mqtt_sender.MqttSender, arduinos: {}, status_service: ServiceClient.StatusServiceClient):
        self.sender = sender
        self.arduinos = arduinos
        self.status_service = status_service

    def execute_action(self, action: object, pins_to_switch: object) -> object:
        if self.check_condition(action.get_condition()):
            logger.info(f"Process action with type '{action.action_type}'")
            if action.action_type == domain.ActionType.TOGGLE:
                action.perform_action(pins_to_switch, self.status_service.get_arduino_pin_status(action.master.parent, action.master.number))
            else:
                action.perform_action(pins_to_switch)
            self.process_notification(action)
        else:
            logger.info(f"Condition not met")

    def button_pressed(self, button: domain.ButtonPin, arduino_name: str):
        # 	if button_hasMulticlick_actions
        #		clicks ++
        #		if button has LongDown triggers
        #       	start button.timer of smallest longdown trigger with Actionclicks = clicks
        #	else
        #   	if button has Immediate triggers
        #       	fire Immediate actions
        #   	if button has LongDown triggers
        #       	start button.timer of smallest longdown trigger
        pins_to_switch = {}
        if button.multi_click_timer is not None:
            button.stop_multi_click_timer()
        if button.has_multi_click_actions(0):
            button.clicks += 1
        else:
            for action in button.get_button_immediate_actions():
                self.execute_action(action, pins_to_switch)
            self.sender.publish_relative_action(pins_to_switch)

        seconds_down = button.get_smallest_longdown_time(0, button.clicks)
        if seconds_down is not None:
            button.start_long_down_timer(seconds_down, self.sender.publish_message_to_button_processor,
                                         [arduino_name, button.number, seconds_down, button.clicks])

    def check_condition(self, condition: domain.Condition):
        if condition is None:
            return True
        if condition.condition_type == domain.ConditionType.TIME:
            return condition.from_time <= datetime.now().time() <= condition.to_time
        elif condition.condition_type == domain.ConditionType.OUTPUT_PIN:
            return condition.status == self.status_service.get_arduino_pin_status(condition.output_pin.parent, condition.output_pin.number)
        elif condition.condition_type == domain.ConditionType.LIST:
            for condition in condition.conditions:
                if condition.operator == domain.Operator.AND:
                    for condition in condition.conditions:
                        if not self.check_condition(condition):
                            return False
                    return True
                    # Otherwise it's OR
                for condition in condition.conditions:
                    if self.check_condition(condition):
                        return True
                    return False
        else:
            logger.warning("Condition not caught")
            return False

    def button_unpressed(self, button: domain.ButtonPin, arduino_name: str):
        #   if clicks > 1
        #       start MulticlickTimer (payload clicks)
        #		if button.timer is running
        #       	cancel timer
        #   else if button.timer is running
        #       cancel timer
        #       if not button.longdown_executed
        #           execute AfterRelease
        #   else
        #       if not button.longdown_executed
        #           fire AfterRelease
        #   remove flag longdown_executed
        logger.debug(f"Number of clicks: {button.clicks}")
        if button.clicks > 0:
            if not button.longdown_executed and button.has_multi_click_actions(button.clicks):
                button.start_multi_click_timer(button.time_between_clicks, self.sender.publish_multiclick_message_to_button_processor,
                                             [arduino_name, button.number, button.clicks])
            else:
                logger.debug(f"reset the button clicks")
                button.clicks = 0
            if button.long_down_timer is not None:
                button.stop_long_down_timer()
        else:
            if button.long_down_timer is not None:
                button.stop_long_down_timer()
            if not button.longdown_executed:
                pins_to_switch = {}
                for action in button.get_button_after_release_actions():
                    logger.debug(f"Execute After release actions")
                    self.execute_action(action, pins_to_switch)
                self.sender.publish_relative_action(pins_to_switch)
        button.longdown_executed = False

    def button_multiclick_fired(self, payload: Dict[str, object]):
        #   if clicks == payload clicks
        #		if button has Immediate triggers with actions_clicks == clicks
        #       	fire Immediate actions
        #		if button has AfterRealse triggers with actions_clicks == clicks
        #       	fire AfterRealse actions
        #		clicks = 1
        json_object = json.loads(payload)
        logger.debug(f"Process Multiclick action")
        clicks = int(json_object['clicks'])
        arduino = self.arduinos.get(json_object['name'], None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return
        button = arduino.button_pins[json_object['button_pin']]
        logger.debug(f"Compair button click {button.clicks} with payload {clicks}")
        if button.clicks == clicks:
            pins_to_switch = {}
            for action in button.get_button_after_release_immediate_actions(button.clicks):
                self.execute_action(action, pins_to_switch)
            self.sender.publish_relative_action(pins_to_switch)
            button.clicks = 0
            button.stop_multi_click_timer()
        else:
            logger.debug(f"New click has been received")
            return

    def button_timer_fired(self, payload: Dict[str,object]):
        #   if button.timer is not running
        #       return
        #   execute LongDown with time passed (don't fire with smaller triggers)
        #   set flag longdown_executed
        #   if button has LongDown with larger triggers
        #       start new button.timer (remember time already passed)
        json_object = json.loads(payload)
        fired_seconds_down = int(json_object['seconds_down'])
        arduino = self.arduinos.get(json_object['name'], None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return
        button = arduino.button_pins[json_object['button_pin']]
        if button.long_down_timer is None:
            return

        pins_to_switch = {}
        for action in button.get_button_long_down_actions(fired_seconds_down):
            self.execute_action(action, pins_to_switch)
        self.sender.publish_relative_action(pins_to_switch)
        button.longdown_executed = True

        seconds_down = button.get_smallest_longdown_time(fired_seconds_down, button.clicks)
        if seconds_down is not None:
            button.start_long_down_timer(seconds_down - fired_seconds_down, self.sender.publish_message_to_button_processor,
                                         [json_object['name'], button.number, seconds_down, button.clicks])
        else:
            button.clicks = 0

    def process_button(self, arduino: domain.Arduino, pin, value: bool):
        button = arduino.button_pins[pin]
        logger.debug(f"button pin: {button.number} with value: {value}")
        if value:
            self.button_pressed(button, arduino.name)
        else:
            self.button_unpressed(button, arduino.name)

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


