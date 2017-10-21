import src.irulez.util as util
import src.irulez.constants as constants
import src.irulez.log as log
from typing import List, Dict, Optional
import json
import src.irulez.domain as domain
import xmlrpc.client

logger = log.get_logger('relative_convertor_mqtt_sender')


class MqttSender:
    def __init__(self, client, serviceConfig: Dict[str,str]):
        self.client = client
        self.serviceConfig = serviceConfig

    def publish_absolute_action(self, json_object: Dict[str, object], absolute: List[bool]):
        payload = util.convert_array_to_hex(absolute)
        topic = json_object['topic']
        logger.debug(f"Publishing: {topic}/{payload}")
        self.client.publish(topic, payload, 0, False)

    def send_absolute_update(self, json_object: Dict[str, object]):

        # Accepts relative pins as input, converts them to absolute updates
        #  Current implementation sends updates to all arduinos or none.

        with xmlrpc.client.ServerProxy(f"http://{self.serviceConfig['url']}:{self.serviceConfig['port']}/") as proxy:
            begin_status = proxy.arduino_status(json_object['name'])
            end_status = begin_status[:]

        for pin in json_object['on']:
            end_status[pin] = True
        for pin in json_object['off']:
            end_status[pin] = False

        logger.debug(f"absolute action: '{end_status}' should_update='{not self.compaire_list(begin_status, end_status)}'")

        if not self.compaire_list(begin_status, end_status):
            self.publish_absolute_action(json_object, end_status)
        else:
            logger.info("No change to publish")

    def compaire_list(seslf, begin_status: List[bool], end_status: List[bool]):
        return begin_status == end_status



