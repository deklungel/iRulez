import src.button.mqtt_sender as mqtt_sender
import src.irulez.log as log
import src.irulez.domain as domain
logger = log.get_logger('button_processor')


class ButtonActionProcessor:
    def __init__(self, sender: mqtt_sender.MqttSender, arduinos: {}):
        self.sender = sender
        self.arduinos = arduinos

    def process_button(self, arduino, pin, value: bool):
        actions = arduino.button_pins[pin].get_button_pin_actions()
        pins_to_switch = {}
        for action in actions:
            if action.should_trigger(value) and action.check_condition():
                logger.info(f"Process action with type '{action.action_type}'")
                action.perform_action(pins_to_switch)
                self.process_notification(action)
            elif not action.check_condition():
                logger.info(f"Condition not met")

        logger.debug(f"Pins to switch: '{pins_to_switch}'")
        self.sender.publish_relative_action(pins_to_switch)

    def process_notification(self,action: domain.Action):
        pass

    def process_button_message(self, name:str, payload: str):
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
