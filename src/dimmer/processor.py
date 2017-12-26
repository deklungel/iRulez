import json
import src.dimmer.mqtt_sender as mqtt_sender
import lib.paho.mqtt.client as mqtt
import src.irulez.log as log
import src.irulez.constants as constants
import src.irulez.util as util
import src.dimmer.domain as domain
from typing import Dict, List
import src.output_status.ServiceClient as ServiceClient

logger = log.get_logger('dimmer_processor')


class DimmerActionProcessor:
    def __init__(self,client: mqtt.Client,  sender: mqtt_sender.MqttSender, status_service: ServiceClient):
        self.sender = sender
        self.client = client
        self.status_service = status_service
        self.buttonLow = {}

    def process_dimmer_message(self, payload: str):
        logger.info("Processing " + payload)
        json_object = json.loads(payload)
        #Payload info
        "name --> arduino name"
        "topic"
        "on"
        "off"
        "delay"
        "speed"
        "dim_light_value"

        name = json_object['name']
        pin_to_swich_off = json_object['off']
        pin_to_swich_on = json_object['on']
        speed = json_object['speed']
        dim_light_value = json_object['dim_light_value']

        #calculate the time between messages
        timer_between_messages = 1000 / constants.dim_frequency_per_sec

        # calculate in how many message the light will go from 100 to 0.
        # f.e. with a speed of 1sec (1000 msec) we have 5 parts
        dim_parts = speed / timer_between_messages
        # calculate the value of very message
        # f.e. with 5 parts every part has a value of 20%
        dim_value = 100 / dim_parts

        for pin in pin_to_swich_off:
            value = self.status_service.get_arduino_pin_status(name, pin)
            if value != 0:
                self.sender.publish_dim_message(pin, name, value, dim_value, timer_between_messages, False)

        for pin in pin_to_swich_on:
            value = self.status_service.get_arduino_pin_status(name, pin)
            if value < dim_light_value:
                self.sender.publish_dim_message(pin, name, value, dim_value, timer_between_messages, True)


    def process_dimmer_real_time_message(self,payload: str):
        logger.info("Processing " + payload)
        json_object = json.loads(payload)

        arduino_name = json_object['arduino_name']
        button_number = json_object['button_number']

        if arduino_name in self.buttonLow.keys():
            if button_number not in self.buttonLow[arduino_name].button_numbers:
                self.buttonLow[arduino_name].button_numbers.append(button_number)
        else:
            self.client.subscribe(constants.arduinoTopic + "/" + arduino_name + "/" + constants.buttonTopic)
            self.buttonLow[arduino_name] = domain.ButtonLow(json_object['button_number'],
                                                                          json_object['number_of_pins'])


        #Payload
        """
        "name" 
        "topic"
        "on" 
        "off"
        "delay"
        "arduino_name" 
        "button_number"
        "speed"
        "dim_light_value"
        "dim_direction_up"
        "number_of_pins
        """
        for pin in list(json_object['on']):
            pass

        for pin in list(json_object['off']):
            pass

    def process_button_message(self, payload: str, name: str):
        if name in self.buttonLow.keys():
            pin_to_remove = []
            status = util.convert_hex_to_array(payload, self.buttonLow[name].number_of_pins)
            for button in self.buttonLow[name].button_numbers:
                if status[button] == 1:
                    return
                #stop the dimmer
                pin_to_remove.append(button)

            #clean up released buttons
            self.buttonLow[name].cleanup()

            #check if arduino needs to be subscribed
            if len(self.buttonLow[name].button_numbers) == 0:
                del self.buttonLow[name]
                self.client.unsubscribe(constants.arduinoTopic + "/" + name + "/" + constants.buttonTopic)

        else:
            logger.warning("We should not receive this messagage from MQTT")
            self.client.unsubscribe(constants.arduinoTopic + "/" + name + "/" + constants.buttonTopic)
