import src.irulez.util as util
import src.irulez.log as log
import src.output_status.ServiceClient as ServiceClient
from typing import List, Dict

logger = log.get_logger('relative_convertor_mqtt_sender')


class MqttSender:
    def __init__(self, client, status_service: ServiceClient.StatusServiceClient):
        self.client = client
        self.status_service = status_service

    def publish_absolute_action(self, json_object: Dict[str, object], absolute: List[bool]):
        payload = util.convert_array_to_hex(absolute)
        topic = json_object['topic']
        logger.debug(f"Publishing: {topic}/{payload}")
        self.client.publish(topic, payload, 0, False)

    def send_absolute_update(self, json_object: Dict[str, object]):

        # Accepts relative pins as input, converts them to absolute updates
        #  Current implementation sends updates to all arduinos or none.


        begin_status = self.status_service.get_arduino_status(str(json_object['name']))
        end_status = begin_status[:]

        # noinspection PyTypeChecker
        for pin in list(json_object['on']):
            end_status[pin] = True
        # noinspection PyTypeChecker
        for pin in list(json_object['off']):
            end_status[pin] = False

        logger.debug(
            f"absolute action: '{end_status}' should_update='{not util.compare_lists(begin_status, end_status)}'")

        if not util.compare_lists(begin_status, end_status):
            self.publish_absolute_action(json_object, end_status)
        else:
            logger.info("No change to publish")
