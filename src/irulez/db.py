import src.irulez.domain as domain
from abc import ABC, abstractmethod


class ArduinoConfig:
    """Represents a database object containing the configuration of an arduino"""
    def __init__(self, name: str, pins: list):
        # Check that all elements in our list are actual ArduinoPin objects
        # This check is completely unnecessary, but gives us some assurances
        all(isinstance(el, domain.ArduinoPin) for el in pins)
        self.name = name
        self.pins = pins


class MqttConfig:
    """Represents the configuration of the mqtt service"""
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port


class DbBase(ABC):
    """Base class, defining all methods a database class should implement"""
    @abstractmethod
    def get_arduino_configs(self) -> ArduinoConfig:
        pass

    @abstractmethod
    def get_mqtt_config(self) -> MqttConfig:
        pass


class DummyDb(DbBase):
    """Dummy implementation of a database class. Returns fixed data for all operations"""
    def get_arduino_configs(self):
        # TODO implement
        pass

    def get_mqtt_config(self):
        return MqttConfig("10.0.50.50", 1883)


def get_dummy_db() -> DbBase:
    """Returns a dummy database"""
    return DummyDb()
