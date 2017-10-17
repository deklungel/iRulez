import src.irulez.util as util
import src.irulez.constants as constants
import src.irulez.log as log
from typing import List, Dict, Optional
import json

logger = log.get_logger('relative_convertor_mqtt_sender')


class MqttSender:
    def __init__(self, client, arduinos: {}):
        self.client = client
        self.arduinos = arduinos

    def publish_absolute_action(self, json_object: {}, absolute: []):
        payload = util.convert_array_to_hex(absolute)
        topic = json_object['topic']
        logger.debug(f"Publishing: {topic}/{payload}")
        self.client.publish(topic, payload, 0, False)

    def send_absolute_update(self, arduino, json_object):

        # Accepts relative pins as input, converts them to absolute updates
        # TODO: improve 'send_update' mechanism to only send updates to arduinos with updates.
        #  Current implementation sends updates to all arduinos or none.
        send_update = False

        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            # Continue means hop to the next cycle of the for loop

        absolute = [False] * arduino.number_of_output_pins
        for pin in arduino.output_pins.values():
            if pin.state:
                absolute[pin.number] = True
            if pin.number in json_object['on'] and not pin.state:
                send_update = True
                absolute[pin.number] = True

        for pin in arduino.output_pins.values():
            if pin.state:
                absolute[pin.number] = True
            if pin.number in json_object['off'] and pin.state:
                absolute[pin.number] = False
                send_update = True

        logger.debug(f"absolute action: '{absolute}' should_update='{send_update}'")

        if send_update:
            self.publish_absolute_action(json_object, absolute)
        else:
            logger.info("No change to publish")




