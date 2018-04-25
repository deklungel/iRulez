import src.dimmer.mqtt_sender as mqtt_sender
import lib.paho.mqtt.client as mqtt
import src.irulez.log as log
import src.irulez.constants as constants
import src.irulez.util as util
import src.dimmer.domain as domain
from typing import List
import src.output_status.ServiceClient as ServiceClient
import uuid

logger = log.get_logger('dimmer_processor')


class DimmerActionProcessor:
    def __init__(self, client: mqtt.Client, sender: mqtt_sender.MqttSender, status_service: ServiceClient):
        self.__sender = sender
        self.__client = client
        self.__status_service = status_service
        # Dictionary with as key a uuid and value a domain.DimmingAction
        self.__dimming_actions = {}

        # Dictionary with as key a button_key and value a uuid (representing the dimming action id)
        # Button_key is a combination of arduino name and button number
        self.__button_cancel_action = {}

    def process_dimmer_message(self, payload: str):
        logger.info("Processing " + payload)
        json_object = util.deserialize_json(payload)
        # Payload info
        # "name --> arduino name"
        # "topic"
        # "pins"
        # "delay"
        # "speed"
        # "dim_light_value"
        # "cancel_on_button_release"
        # "arduino_name"
        # "button_number"

        # Get data from payload
        name = util.get_str_from_json_object(json_object, 'name')
        pins_to_switch = util.get_int_list_from_json_object(json_object, 'pins')
        speed = util.get_int_from_json_object(json_object, 'speed')
        dim_light_value = util.get_int_from_json_object(json_object, 'dim_light_value')
        cancel_on_button_release = util.get_bool_from_json_object(json_object, 'cancel_on_button_release')
        arduino_name = util.get_str_from_json_object(json_object, 'arduino_name')
        button_number = util.get_int_from_json_object(json_object, 'button_number')

        # Calculate the time between messages
        timer_between_messages = int(1000 / constants.dim_frequency_per_sec)

        # calculate in how many message the light will go from 100 to 0.
        # f.e. with a speed of 1sec (1000 msec) we have 5 parts
        number_of_parts = int(speed / timer_between_messages)
        if number_of_parts < 1:
            number_of_parts = 1

        # Create dimming action, containing all needed information
        dimming_action = domain.DimmingAction(name, timer_between_messages)
        for pin in pins_to_switch:
            # For each pin, calculate the values that need to be sent to the arduino for each message
            current_value = self.__status_service.get_arduino_dim_pin_status(name, pin)
            interval_values = self.__get_interval_values(number_of_parts, current_value, dim_light_value)
            dimming_action.add_pin(domain.PinWithIntervals(pin, interval_values))

        # Add the dimming action to the dictionary
        dimming_action_id = uuid.uuid4()
        self.__dimming_actions[dimming_action_id] = dimming_action

        if cancel_on_button_release:
            self.__button_cancel_action[arduino_name + str(button_number)] = dimming_action_id

        # Send message to the timer module to time the first dimming message
        self.__sender.publish_dimming_action_to_timer(dimming_action_id, timer_between_messages)

    def __get_interval_values(self, number_of_parts: int, start_value: int, end_value: int) -> List[int]:
        step = (end_value - start_value) / float(number_of_parts)
        to_return = []
        current = float(start_value)
        for i in range(0, number_of_parts):
            current += step
            to_return.append(int(current))

        return to_return

    def process_dimmer_timer_fired(self, payload: str):
        """
        Check if dimming isn't stopped yet
        Check if it's the last message, otherwise send new message to timer module
        Send mqtt message(s) to arduino to actually dim
        """
        dimming_action_id = uuid.UUID(payload)
        dimming_action = self.__dimming_actions.get(dimming_action_id, None)
        if dimming_action is None:
            logger.error(f"Received dimmer timer fired message of id '{dimming_action_id}', but action not found")
            return

        if not isinstance(dimming_action, domain.DimmingAction):
            logger.error(f"Found object for dimming action id '{dimming_action_id}', "
                         f"but it wasn't a domain.DimmingAction")
            return

        if dimming_action.stopped:
            return

        if not dimming_action.is_final_step():
            self.__sender.publish_dimming_action_to_timer(dimming_action_id, dimming_action.interval_time_between)
        else:
            del(self.__dimming_actions[dimming_action_id])

        for pin_with_interval in dimming_action.get_current_pins_with_interval():
            self.__sender.publish_dimming_action_to_arduino(dimming_action.arduino_name, pin_with_interval[0],
                                                            pin_with_interval[1])

        dimming_action.increment_step()

    def process_dimmer_cancelled(self, payload: str):
        logger.info("Processing " + payload)
        json_object = util.deserialize_json(payload)
        # Payload info
        # "arduino_name"
        # "button_number"

        arduino_name = util.get_str_from_json_object(json_object, 'arduino_name')
        button_number = util.get_int_from_json_object(json_object, 'button_number')
        key = arduino_name + str(button_number)

        action_uuid_to_cancel = self.__button_cancel_action.get(key, None)
        if action_uuid_to_cancel is None:
            logger.info(f"No action to cancel found for arduino {arduino_name}, button {button_number}")
            return

        dimming_action = self.__dimming_actions.get(action_uuid_to_cancel, None)
        if dimming_action is None:
            logger.warn(f"Received dimmer timer fired message of id '{action_uuid_to_cancel}', but action not found")
            return

        if not isinstance(dimming_action, domain.DimmingAction):
            logger.error(f"Found object for dimming action id '{action_uuid_to_cancel}', "
                         f"but it wasn't a domain.DimmingAction")
            return

        dimming_action.stop()
        del(self.__button_cancel_action[key])
