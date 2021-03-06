from abc import ABC, abstractmethod
from typing import List, Optional


class Service(ABC):
    @abstractmethod
    def get_arduino_status(self, name: str) -> List[bool]:
        pass

    @abstractmethod
    def get_arduino_pin_status(self, name: str, pin: int) -> Optional[bool]:
        pass

    @abstractmethod
    def get_arduino_dim_pin_status(self, name: str, pin: int) -> Optional[str]:
        pass

    @abstractmethod
    def get_dimmer_light_value(self, name: str, id: int) -> Optional[int]:
        pass

