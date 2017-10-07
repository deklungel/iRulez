import src.irulez.util as util
import src.irulez.constants as constants
import src.irulez.log as log

logger = log.get_logger('mqtt_sender')


def convert_individual_pins_to_complete_array(individual_pins: [], array_length: int) -> []:
    to_return = [False] * array_length
    for pin in individual_pins:
        to_return[pin] = True
    return to_return


class MqttSender:
    def __init__(self, client, arduinos: {}):
        self.client = client
        self.arduinos = arduinos

    def publish_action(self, absolute):
        for name in absolute:
            payload = util.convert_array_to_hex(absolute[name])
            topic = constants.arduinoTopic + '/' + name + '/' + constants.actionTopic
            logger.debug(f"Publishing: {topic}/{payload}")
            self.client.publish(topic, payload, 0, True)

    def publish_relative_action(self, relative: str):
        for name in relative:
            payload = relative[name].replace('||', '|')
            topic = constants.arduinoTopic + '/' + name + '/' + constants.actionTopic + '/' + constants.relative
            logger.debug(f"Publishing: {topic}/{relative[name]}")
            self.client.publish(topic, payload, 0, False)

    def publish_absolute_action(self, name: str, absolute: []):
        payload = util.convert_array_to_hex(absolute)
        topic = constants.arduinoTopic + '/' + name + '/' + constants.actionTopic
        logger.debug(f"Publishing: {topic}/{payload}")
        #self.client.publish(topic, payload, 0, True)

    def send_absolute_update(self,name: list, on_pins: list, off_pins: int):
        # Accepts relative pins as input, converts them to absolute updates
        # TODO: improve 'send_update' mechanism to only send updates to arduinos with updates.
        #  Current implementation sends updates to all arduinos or none.
        send_update = False

        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            # Continue means hop to the next cycle of the for loop

        absolute = [False] * arduino.number_of_output_pins
        for pin in arduino.output_pins.values():
            if pin.state:
                absolute[pin.number] = True
            if on_pins[pin.number] and not pin.state:
                send_update = True
                absolute[pin.number] = True

        for pin in arduino.output_pins.values():
            if pin.state:
                absolute[pin.number] = True
            if off_pins[pin.number] and pin.state:
                absolute[pin.number] = False
                send_update = True

        logger.debug(f"absolute: '{absolute}'")
        if send_update:
            self.publish_absolute_action(name, absolute)
        else:
            logger.info("No change to publish")

    # TODO: Delete send_absolute_update2
    def send_absolute_update2(self, on_pins: {}, off_pins: {}):
        # Accepts relative pins as input, converts them to absolute updates
        # TODO: improve 'send_update' mechanism to only send updates to arduinos with updates.
        #  Current implementation sends updates to all arduinos or none.
        send_update = False
        absolute = {}
        for name in on_pins:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                # Continue means hop to the next cycle of the for loop
                continue
            absolute[name] = [False] * arduino.number_of_output_pins
            for pin in arduino.output_pins.values():
                if pin.state:
                    absolute[name][pin.number] = True
                if on_pins[name][pin.number] and not pin.state:
                    send_update = True
                    absolute[name][pin.number] = True

        for name in off_pins:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                return
            if name not in absolute.keys():
                absolute[name] = [False] * arduino.number_of_output_pins
            for pin in arduino.output_pins.values():
                if pin.state:
                    absolute[name][pin.number] = True
                if off_pins[name][pin.number] and pin.state:
                    absolute[name][pin.number] = False
                    send_update = True

        logger.debug(f"absolute: '{absolute}'")
        if send_update:
            self.publish_action(absolute)
        else:
            logger.info("No change to publish")

    def send_relative_update(self, pins_to_switch_on: {}, pins_to_switch_off: {}):
        # Accepts a dictionary with as key arduino name and value an array of pins to change
        on_pins = {}
        off_pins = {}
        logger.debug('Convert on pins')
        self.convert_individual_pins_dict_to_complete_array_dict(pins_to_switch_on, on_pins)
        logger.debug('Convert off pins')
        self.convert_individual_pins_dict_to_complete_array_dict(pins_to_switch_off, off_pins)
        logger.debug(f"on Pins: '{on_pins}' & off pins: '{off_pins}'")

        relative = {}
        for name in on_pins:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                # Continue means hop to the next cycle of the for loop
                continue
            relative[name] = util.convert_array_to_hex(on_pins[name])  + "|"
            logger.debug(f"Arduino '{name}' hex value '{relative[name]}'")

        for name in off_pins:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                # Continue means hop to the next cycle of the for loop
                continue
            if name not in relative.keys():
                relative[name] = ""
            relative[name] = relative[name] + "|" + util.convert_array_to_hex(off_pins[name])

        # TODO: change send_absolute_update to publish_relative_action

        self.send_absolute_update2(on_pins, off_pins)
        #self.publish_relative_action(relative)


    def convert_individual_pins_dict_to_complete_array_dict(self, individual_pins: {}, complete_array: {}):
        logger.debug(f"Individual pins: '{individual_pins}'")
        for name in individual_pins:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                return
            complete_array[name] = convert_individual_pins_to_complete_array(individual_pins[name],
                                                                             arduino.number_of_output_pins)
