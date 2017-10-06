import src.communication.mqtt_sender as mqtt_sender
import src.irulez.log as log

logger = log.get_logger('button_processor')


class ButtonActionProcessor:
    def __init__(self, sender: mqtt_sender.MqttSender, arduinos: {}):
        self.sender = sender
        self.arduinos = arduinos

    def process_button(self, arduino, pin, value: bool):
        actions = arduino.button_pins[pin].get_button_pin_actions()
        pins_to_switch_on = {}
        pins_to_switch_off = {}
        for action in actions:
            if action.should_trigger(value) and action.check_condition():
                logger.info(f"Process action with type '{action.action_type}'")
                action.perform_action(pins_to_switch_on, pins_to_switch_off)
            elif not action.check_condition():
                logger.info(f"Condition not met")

        logger.debug(f"Pins to switch on: '{pins_to_switch_on}' & Pins to switch off: '{pins_to_switch_off}'")
        self.sender.send_relative_update(pins_to_switch_on, pins_to_switch_off)

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
    def process_button_message(self, name, payload):
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

    def update_arduino_output_pins(self, name, payload):
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return
        logger.debug(f"Board with name '{name}' found")
        arduino.set_output_pin_status(payload)
        logger.debug(f"relay status HEX: '{arduino.get_output_pin_status()}'.")
