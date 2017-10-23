from abc import ABC, abstractmethod
from typing import List

class Service(ABC):
    @abstractmethod
    def get_arduino_status(self, name: str) -> List[str]:
        pass

