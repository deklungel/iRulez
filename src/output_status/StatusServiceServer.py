import src.output_status.service_domain as service
import threading
from typing import List
import src.irulez.log as log
from xmlrpc.server import SimpleXMLRPCServer

logger = log.get_logger('StatusServiceServer')


class ServiceServer(service.Service):
    def __init__(self, arduinos: object, url: object, port: object) -> object:
        self.arduinos = arduinos
        self.url = url
        self.port = port

    def connect(self):
        server = SimpleXMLRPCServer((self.url, self.port))
        logger.info(f"Listening on port {port}...")
        server.register_function(self.status, "status")
        server.register_function(self.get_arduino_status, "arduino_status")
        server.register_multicall_functions()
        th = threading.Thread(target=server.serve_forever)
        th.deamon = True
        th.start()

    def status(self, name: str, pin: int) -> bool:
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return "ERROR"
        status = arduino.output_pins[pin].state
        return status

    def get_arduino_status(self, name: str) -> List[bool]:
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return "ERROR"
        status = []
        for pin in arduino.output_pins.values():
            status.append(pin.state)
        return status
