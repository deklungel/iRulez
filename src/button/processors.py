import src.communication.mqtt_sender as mqtt_sender
import src.irulez.domain as domain
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
            if action.trigger.get_action_trigger_type() == domain.ActionTriggerType.IMMEDIATELY and value:
                logger.info(f"Process action Immediatly")
                if(action.action_type == domain.ActionType.ON):
                    logger.debug("ON action")
                    pins = action.output_pins
                    for pin in pins:
                        logger.debug(f"Action ON for pin '{pin.number}'")
                        pins_to_switch_on.setdefault(pin.parent, []).append(pin.number)
                elif(action.action_type == domain.ActionType.OFF):
                    logger.debug("OFF action")
                    pins = action.output_pins
                    for pin in pins:
                        pins_to_switch_off.setdefault(pin.parent, []).append(pin.number)
                elif (action.action_type == domain.ActionType.TOGGLE):
                    logger.debug("Toggle action")
            elif action.trigger.get_action_trigger_type() == domain.ActionTriggerType.AFTER_RELEASE and value == False:
                logger.info(f"Process action After Release")

        self.sender.send_relative_update(pins_to_switch_on, pins_to_switch_off)

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
        arduino.set_relay_status(payload)
        logger.debug(f"relay status HEX: '{arduino.get_relay_status()}'.")
