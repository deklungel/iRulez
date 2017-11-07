import threading
from typing import List, Dict, Optional
from xmlrpc.server import SimpleXMLRPCServer
import src.output_status.domain as domain
import src.irulez.log as log
import src.output_status.service_domain as service

logger = log.get_logger('StatusServiceServer')


class OutputServiceServer(service.Service):
    def __init__(self, arduinos: Dict[str, domain.Arduino], url: object, port: object):
        self.arduinos = arduinos
        self.url = url
        self.port = port

    def connect(self) -> None:
        server = SimpleXMLRPCServer((self.url, self.port))
        logger.info(f"Listening on port {self.port}...")
        server.register_function(self.get_arduino_pin_status, "arduino_pin_status")
        server.register_function(self.get_arduino_status, "arduino_status")
        server.register_multicall_functions()
        th = threading.Thread(target=server.serve_forever)
        th.daemon = True
        th.start()

    def get_arduino_pin_status(self, name: str, pin: int) -> Optional[bool]:
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return None
        status = arduino.output_pins[pin].state
        return status

    def get_arduino_status(self, name: str) -> List[bool]:
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return []
        status = []
        for pin in arduino.output_pins.values():
            status.append(pin.state)
        return status
