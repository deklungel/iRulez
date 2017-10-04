import src.irulez.db_domain as db_domain
from abc import ABC, abstractmethod
from datetime import time
from typing import List


class DbBase(ABC):
    """Base class, defining all methods a database class should implement"""

    @abstractmethod
    def get_arduinos(self) -> List[db_domain.Arduino]:
        """Retrieves the arduinos as they are known in the database"""
        pass

    @abstractmethod
    def get_templates(self) -> List[db_domain.Template]:
        """Retrieves the templates as they are known in the database"""
        pass

    @abstractmethod
    def get_input_pins(self) -> List[db_domain.InputPin]:
        """Retrieves the input pins as they are known in the database"""
        pass

    @abstractmethod
    def get_output_pins(self) -> List[db_domain.OutputPin]:
        """Retrieves the output pins as they are known in the database"""
        pass

    @abstractmethod
    def get_actions(self) -> List[db_domain.Action]:
        """Retrieves the actions as they are known in the database"""
        pass

    @abstractmethod
    def get_triggers(self) -> List[db_domain.Trigger]:
        """Retrieves the triggers as they are known in the database"""
        pass

    @abstractmethod
    def get_conditions(self) -> List[db_domain.Condition]:
        """Retrieves the conditions as they are known in the database"""
        pass


class DummyDb(DbBase):
    """Dummy implementation of a database class. Returns fixed data for all operations"""

    def get_templates(self) -> List[db_domain.Template]:
        return [db_domain.Template(0, "16x16 Template", 16, 16)]

    def get_arduinos(self) -> List[db_domain.Arduino]:
        return [db_domain.Arduino(0, "DEMO", 0)]

    def get_output_pins(self) -> List[db_domain.OutputPin]:
        to_return = []
        for x in range(0, 16):
            to_return.append(db_domain.OutputPin(x, x, 0))
        return to_return

    def get_triggers(self) -> List[db_domain.Trigger]:
        return [db_domain.Trigger(0, 1, None, None)]

    def get_conditions(self) -> List[db_domain.Condition]:
        return [db_domain.Condition(0, 3, None, None, None, None, time(9, 0), time(12, 00)),
                db_domain.Condition(1, 3, None, None, None, None, time(18, 0), time(23, 59)),
                db_domain.Condition(2, 1, 2, [0, 1], None, None, None, None),
                db_domain.Condition(3, 2, None, None, 15, True, None, None),
                db_domain.Condition(4, 1, 1, [2, 3], None, None, None, None)]

    def get_actions(self) -> List[db_domain.Action]:
        # Create 3 actions.
        # Action 1 execute immediately, pins 0 and 10 ON, condition 4
        # Action 2 execute immediately, pins 2 and 9 OFF
        # Action 3 execute immediately, ping 8,9,10 TOGGLE, master 8
        return [db_domain.Action(0, 2, 0, 0, [0, 10], 4, None),
                db_domain.Action(1, 3, 0, 0, [2, 9], None, None),
                db_domain.Action(2, 1, 0, 0, [8, 9, 10], None, 8)]

    def get_input_pins(self) -> List[db_domain.InputPin]:
        to_return = []
        for x in range(0, 16):
            to_return.append(db_domain.InputPin(x, x, [], 0))

        to_return[5].action_ids.extend([0, 1])
        to_return[10].action_ids.extend([2])

        return to_return


def get_dummy_db() -> DbBase:
    """Returns a dummy database"""
    return DummyDb()
