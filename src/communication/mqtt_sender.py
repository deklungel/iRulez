import src.irulez.util as util
import src.irulez.constants as constants
import src.irulez.log as log
from typing import List, Dict, Optional
import json

logger = log.get_logger('mqtt_sender')



class JsonMessage:
    def __init__(self, delay: int, on: [], off :[]):
        self.on = on
        self.off = off
        self.delay = delay


class MqttSender:
    def __init__(self, client, arduinos: {}):
        self.client = client
        self.arduinos = arduinos

    def publish_relative_action(self, jsonList: {}):
        for name in jsonList:
            for i in range(len(jsonList[name])):
                payload = json.dumps({"on": jsonList[name][i].on, "off": jsonList[name][i].off, "delay": jsonList[name][i].delay})
                if(jsonList[name][i].delay == 0):
                    topic = constants.arduinoTopic + '/' + name + '/' + constants.actionTopic + '/' + constants.relative
                else:
                    topic = constants.arduinoTopic + '/' + name + '/' + constants.actionTopic + '/' + constants.relative + '/' + constants.timer
                logger.debug(f"Publishing: {topic}/{payload}")
                self.client.publish(topic, payload, 0, False)


    def publish_absolute_action(self, name: str, absolute: []):
        payload = util.convert_array_to_hex(absolute)
        topic = constants.arduinoTopic + '/' + name + '/' + constants.actionTopic
        logger.debug(f"Publishing: {topic}/{payload}")
        self.client.publish(topic, payload, 0, False)

    def send_absolute_update(self, arduino, onpins: [],offpins: []):
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
            if pin.number in onpins and not pin.state:
                send_update = True
                absolute[pin.number] = True

        for pin in arduino.output_pins.values():
            if pin.state:
                absolute[pin.number] = True
            if pin.number in offpins  and pin.state:
                absolute[pin.number] = False
                send_update = True

        logger.debug(f"absolute action: '{absolute}' should_ipdate='{send_update}'")

        if send_update:
            self.publish_absolute_action(arduino.name, absolute)
        else:
            logger.info("No change to publish")


    def send_relative_update(self, pins_to_switch_on: {}, pins_to_switch_off: {}):
        # Accepts a dictionary with as key arduino name and value an array of pins to change

        jsonlist = {}

        for name in pins_to_switch_on:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                # Continue means hop to the next cycle of the for loop
                continue

            for i in range (len(pins_to_switch_on[name])):
                if(pins_to_switch_on[name][i].delay > 0):
                    jsonlist.setdefault(name, []).append(JsonMessage(pins_to_switch_on[name][i].delay, pins_to_switch_on[name][i].pinNumbers, []))
                else:
                    pins = []
                    for j in range(len(pins_to_switch_on[name][i].pinNumbers)):
                        pins.append(pins_to_switch_on[name][i].pinNumbers[j])
                    jsonlist.setdefault(name, []).append(JsonMessage(pins_to_switch_on[name][i].delay, pins, []))

        for name in pins_to_switch_off:
            arduino = self.arduinos.get(name, None)
            if arduino is None:
                # Unknown arduino
                logger.info(f"Could not find arduino with name '{name}'.")
                # Continue means hop to the next cycle of the for loop
                continue
            for i in range (len(pins_to_switch_off[name])):
                if(pins_to_switch_off[name][i].delay > 0):
                    jsonlist.setdefault(name, []).append(JsonMessage(pins_to_switch_off[name][i].delay,[], pins_to_switch_off[name][i].pinNumbers))
                else:
                    pins = []
                    for j in range(len(pins_to_switch_off[name][i].pinNumbers)):
                        pins.append(pins_to_switch_off[name][i].pinNumbers[j])

            json = jsonlist.get(name, None)
            if json is None:
                jsonlist.setdefault(name, []).append(JsonMessage(pins_to_switch_off[name][i].delay, [], pins))
            else:
                for j in range(len(json)):
                    if json[j].delay == 0:
                        json[j].off = pins
                    continue

        self.publish_relative_action(jsonlist)




