import threading
from typing import List, Dict, Optional
from xmlrpc.server import SimpleXMLRPCServer
import src.output_status.domain as domain
import src.irulez.log as log
import src.output_status.service_domain as service
import src.irulez.util as util

logger = log.get_logger('StatusServiceServer')


class OutputServiceServer(service.Service):

    def __init__(self,
                 arduinos: Dict[str, domain.Arduino],
                 dimmer_light_values: Dict[int, domain.DimmerLightValue],
                 url: object,
                 port: object):
        self.arduinos = arduinos
        self.url = url
        self.port = port
        self.__dimmer_light_values = dimmer_light_values

    def connect(self) -> None:
        server = SimpleXMLRPCServer((self.url, self.port))
        logger.info(f"Listening on port {self.port}...")
        server.register_function(self.get_arduino_pin_status, "arduino_pin_status")
        server.register_function(self.get_arduino_dim_pin_status, "arduino_pin_dim_status")
        server.register_function(self.get_arduino_status, "arduino_status")
        server.register_function(self.get_dimmer_light_value, "dimmer_light_value")

        server.register_function(self.test, "GET")
        server.register_multicall_functions()
        th = threading.Thread(target=server.serve_forever)
        th.daemon = True
        th.start()

    @property
    def dimmer_light_values(self) -> Dict[int, domain.DimmerLightValue]:
        return self.__dimmer_light_values

    def get_arduino_pin_status(self, name: str, pin: int) -> Optional[bool]:
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return None
        return arduino.output_pins[pin].state

    def get_arduino_dim_pin_status(self, name: str, pin: int) -> Optional[str]:
        arduino = self.arduinos.get(name, None)
        if arduino is None:
            # Unknown arduino
            logger.info(f"Could not find arduino with name '{name}'.")
            return None
        return util.serialize_json(
            {
                "state": arduino.output_pins[pin].dim_state,
                "direction": arduino.output_pins[pin].direction
            }
        )

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

    def get_dimmer_light_value(self, name: str, id: int) -> Optional[int]:
        dimmer_light_value = self.dimmer_light_values.get(id, None)
        if dimmer_light_value is None:
            return 100
        return dimmer_light_value.last_light_value

    def test(self) -> str:
        return "Hello World"
