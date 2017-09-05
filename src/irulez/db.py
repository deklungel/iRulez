import src.irulez.domain as domain
from abc import ABC, abstractmethod


class DbBase(ABC):
    """Base class, defining all methods a database class should implement"""
    @abstractmethod
    def get_arduino_config(self) -> domain.ArduinoConfig:
        """Retrieves the configuration of the arduinos"""
        pass

    @abstractmethod
    def get_mqtt_config(self) -> domain.MqttConfig:
        """Retrieves the configuration of mqtt"""
        pass


class DummyDb(DbBase):
    """Dummy implementation of a database class. Returns fixed data for all operations"""
    def __init(self):
        pass

    def get_arduino_config(self):
        # Create array of 16 relay pins
        pins = []
        for x in range(0, 16):
            pins.append([])
            pins[x]= domain.ArduinoPin(x, domain.ArduinoPinType.RELAY)
        # Initialize an arduino with those pins
        arduino = domain.Arduino("dummy", pins)

        # Initialize the dictionary of arduinos (contains only 1 for now)
        # Key is name of the arduino
        return domain.ArduinoConfig([arduino])

    def get_mqtt_config(self):
        return domain.MqttConfig("10.0.50.50", 1883, "iRulezMqtt", "iRulez4MQTT")

class MySQL(DbBase):
    def get_mqtt_config(self) -> domain.MqttConfig:
        pass

    def get_arduino_config(self) -> domain.ArduinoConfig:
        pass


def get_dummy_db() -> DbBase:
    """Returns a dummy database"""
    return DummyDb()
