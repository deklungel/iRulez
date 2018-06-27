import src.output_status.service_domain as service
import xmlrpc.client
from typing import List, Optional
import src.irulez.log as log

logger = log.get_logger('StatusServiceClient')


class StatusServiceClient(service.Service):

    def __init__(self, url: str, port: int):
        self.url = url
        self.port = port

    def get_arduino_status(self, name: str) -> List[bool]:
        with xmlrpc.client.ServerProxy(f"http://{self.url}:{self.port}/") as proxy:
            status = proxy.arduino_status(name)
        logger.debug(f"status: {str(status)}")
        return status

    def get_arduino_pin_status(self, name: str, pin: int) -> bool:
        with xmlrpc.client.ServerProxy(f"http://{self.url}:{self.port}/") as proxy:
            status = proxy.arduino_pin_status(name, pin)
        logger.debug(f"status: {str(status)}")
        return status

    def get_arduino_dim_pin_status(self, name: str, pin: int) -> str:
        with xmlrpc.client.ServerProxy(f"http://{self.url}:{self.port}/") as proxy:
            status = proxy.arduino_pin_dim_status(name, pin)
        logger.debug(f"status: {str(status)}")
        return status

    def get_dimmer_light_value(self, id: int) -> Optional[int]:
        with xmlrpc.client.ServerProxy(f"http://{self.url}:{self.port}/") as proxy:
            status = proxy.dimmer_light_value(id)
        logger.debug(f"status: {str(status)}")
        return status

