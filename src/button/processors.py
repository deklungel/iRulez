import json
from typing import Dict
import src.button.domain as domain
import src.button.action_executor as executor
import src.irulez.log as log
import src.button.mqtt_sender as mqtt_sender

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

    def __init__(self, action_executor: executor.ActionExecutor, arduinos: {}, sender: mqtt_sender.MqttSender):
        self.__action_executor = action_executor
        self.__sender = sender
        self.arduinos = arduinos

    def button_pressed(self, button: domain.ButtonPin, arduino: domain.Arduino):
        """
        if button_hasMulticlick_actions
            clicks ++
        if button has LongDown triggers
            start button.timer of smallest longdown trigger with Actionclicks = clicks
        else
            if button has Immediate triggers
                fire Immediate actions
            if button has LongDown triggers
                start button.timer of smallest longdown trigger
        """
        logger.debug(f"Button {arduino.name}/button{button.number} pressed")

        if button.multi_click_timer is not None:
            button.stop_multi_click_timer()
        if button.has_multi_click_actions(0):
            button.clicks += 1
        else:
            button.clicks = 1

        logger.debug(f"Get immediate actions")
        self.__action_executor.execute_actions(button.get_button_immediate_actions(), button, arduino.name)

        seconds_down = button.get_smallest_longdown_time(0)
        if seconds_down is not None:
            button.start_long_down_timer(seconds_down, self.__sender.publish_message_to_button_processor,
                                         [arduino.name, button.number, seconds_down, button.clicks])

    def button_unpressed(self, button: domain.ButtonPin, arduino: domain.Arduino):
        """
        if clicks > 1
            start MulticlickTimer (payload clicks)
            if button.timer is running
                cancel timer
        else if button.timer is running
            cancel timer
            if not button.longdown_executed
                execute AfterRelease
        else
            if not button.longdown_executed
                fire AfterRelease
        remove flag longdown_executed
        """
        logger.debug(f"Number of clicks: {button.clicks}")
        if button.clicks > 0:
            if not button.longdown_executed and button.has_multi_click_actions(button.clicks):
                button.start_multi_click_timer(int(button.time_between_clicks),
                                               self.__sender.publish_multiclick_message_to_button_processor,
                                               [arduino, button.number, button.clicks])
            else:
                logger.debug(f"reset the button clicks")
                button.clicks = 0
            if button.long_down_timer is not None:
                button.stop_long_down_timer()
        else:
            if button.long_down_timer is not None:
                button.stop_long_down_timer()
            if not button.longdown_executed:
                self.__action_executor.execute_actions(button.get_button_after_release_actions(), button, arduino.name)
        button.longdown_executed = False

    def button_multiclick_fired(self, payload: Dict[str, object]):
        """
            if clicks == payload clicks
                if button has Immediate triggers with actions_clicks == clicks
                    fire Immediate actions
                if button has AfterRelease triggers with actions_clicks == clicks
                    fire AfterRelease actions
                clicks = 1
        """
        json_object = json.loads(payload)
        logger.debug(f"Process Multiclick action")
        clicks = int(json_object['clicks'])
        arduino_name = json_object['name']
        arduino = self.arduinos.get(arduino_name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{arduino_name}'.")
            return
        button = arduino.button_pins[json_object['button_pin']]
        logger.debug(f"Compare button click {button.clicks} with payload {clicks}")
        if button.clicks == clicks:
            self.__action_executor.execute_actions(button.get_button_after_release_actions(button.clicks), button,
                                                   arduino.name)
            button.clicks = 0
            button.stop_multi_click_timer()
        else:
            logger.debug(f"New click has been received")
            return

    def button_timer_fired(self, payload: Dict[str, object]):
        #   if button.timer is not running
        #       return
        #   execute LongDown with time passed (don't fire with smaller triggers)
        #   set flag longdown_executed
        #   if button has LongDown with larger triggers
        #       start new button.timer (remember time already passed)
        json_object = json.loads(payload)
        fired_seconds_down = int(json_object['seconds_down'])
        arduino_name = json_object['name']
        arduino = self.arduinos.get(arduino_name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{arduino_name}'.")
            return
        button = arduino.button_pins[json_object['button_pin']]
        if button.long_down_timer is None:
            return

        self.__action_executor.execute_actions(button.get_button_long_down_actions(fired_seconds_down), button,
                                               arduino.name)
        button.longdown_executed = True

        seconds_down = button.get_smallest_longdown_time(fired_seconds_down, button.clicks)
        if seconds_down is not None:
            button.start_long_down_timer(seconds_down - fired_seconds_down,
                                         self.__sender.publish_message_to_button_processor,
                                         [json_object['name'], button.number, seconds_down, button.clicks])
        else:
            button.clicks = 0

    def process_button(self, arduino: domain.Arduino, pin, value: bool):
        button = arduino.button_pins[pin]
        logger.debug(f"button pin: {button.number} with value: {value}")
        if value:
            self.button_pressed(button, arduino)
        else:
            self.button_unpressed(button, arduino)

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
