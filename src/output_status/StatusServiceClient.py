import src.output_status.service_domain as service
import xmlrpc.client
from typing import List
import src.irulez.log as log

logger = log.get_logger('StatusServiceServer')

class ServiceClient(service.Service):
    def __init__(self, url: str, port: int):
        self.url = url
        self.port = port

    def get_arduino_status(self, name: str) -> List[str]:
        status = []
        with xmlrpc.client.ServerProxy(f"http://{self.url}:{self.port}/") as proxy:
            status = proxy.arduino_status(name)
        log.debug(f"status: {str(status)}")
        return status

    def status(self, name: str, pin: int) -> bool:
        pass
