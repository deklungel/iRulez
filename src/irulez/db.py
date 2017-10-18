import src.irulez.db_domain as db_domain
import lib.mysql.connector as mariadb
from abc import ABC, abstractmethod
from datetime import time
from typing import List
import src.irulez.configuration as configuration
from contextlib import closing

# Configuration
config = configuration.Configuration()
databaseConfig = config.get_database_config()


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

    @abstractmethod
    def get_notifications(self) -> List[db_domain.Notification]:
        """Retrieves the notification as they are known in the database"""
        pass


class DummyDb(DbBase):
    """Dummy implementation of a database class. Returns fixed data for all operations"""

    def get_templates(self) -> List[db_domain.Template]:
        return [db_domain.Template(0, "16x16 Template", 16, 16), db_domain.Template(1, "50x50 Template", 50, 50)]

    def get_arduinos(self) -> List[db_domain.Arduino]:
        return [db_domain.Arduino(0, "DEMO", 0), db_domain.Arduino(1, "virtual_IO_Board", 1)]

    def get_output_pins(self) -> List[db_domain.OutputPin]:
        to_return = []
        for x in range(0, 16):
            to_return.append(db_domain.OutputPin(x, x, 0))
        for x in range(16, 66):
            to_return.append(db_domain.OutputPin(x, x - 16, 1))
        return to_return

    def get_triggers(self) -> List[db_domain.Trigger]:
        return [db_domain.Trigger(0, 1, None, None)]

    def get_conditions(self) -> List[db_domain.Condition]:
        return [db_domain.Condition(0, 3, None, None, None, None, time(9, 0), time(12, 00)),
                db_domain.Condition(1, 3, None, None, None, None, time(18, 0), time(23, 59)),
                db_domain.Condition(2, 1, 2, [0, 1], None, None, None, None),
                db_domain.Condition(3, 2, None, None, 15, True, None, None),
                db_domain.Condition(4, 1, 1, [2, 3], None, None, None, None)]

    def get_notifications(self) -> List[db_domain.Notification]:
        return [db_domain.Notification(0, "Our First Mail Notification", 0, True, "Subject", ["laurentmichel@me.com"], None),
                db_domain.Notification(1, "Our First Telegram Notification", 1, True, None, None, ["token1","token2"])]


    def get_actions(self) -> List[db_domain.Action]:
        # Create 3 actions for arduino 'DEMO".
        # Action 0 execute immediately, pins 0 and 10 ON, condition 4 for 15sec
        # Action 1 execute immediately, pins 2 and 9 OFF
        # Action 2 execute immediately, ping 8,9,10 TOGGLE, master 8, after 30 sec
        return [db_domain.Action(0, 2, 0, [0, 1], 0, 15, [0, 10], 4, None),
                db_domain.Action(1, 3, 0, None, 0, 0, [2, 9], None, None),
                db_domain.Action(2, 1, 0, [0,1], 30, 0, [8, 9, 10], None, 8)]


    def get_input_pins(self) -> List[db_domain.InputPin]:
        to_return = []
        for x in range(0, 16):
            to_return.append(db_domain.InputPin(x, x, [], 0))
        for x in range(16, 66):
            to_return.append(db_domain.InputPin(x, x - 16, [], 1))

        to_return[5].action_ids.extend([0, 1])
        to_return[10].action_ids.extend([2])

        return to_return


class MariaDB(DbBase):

    def __init__(self, ip: str, port: int, username: str, password: str, database: str):
        self.database = database
        self.password = password
        self.username = username
        self.port = port
        self.ip = ip

    def get_templates(self) -> List[db_domain.Template]:
        with closing(self.__create_connection()) as conn:
            with closing(conn.cursor(buffered=True)) as cursor:
                cursor.execute("SELECT id, name, nb_input_pins, nb_output_pins FROM tbl_Template")
                templates = []
                for id, name, nb_input_pins, nb_output_pins in cursor:
                    templates.append(db_domain.Template(id, name, nb_input_pins, nb_output_pins))
        return templates

    def get_arduinos(self) -> List[db_domain.Arduino]:
        with closing(self.__create_connection()) as conn:
            with closing(conn.cursor(buffered=True)) as cursor:
                cursor.execute("SELECT id, name, template_id FROM tbl_Arduino")
                arduinos = []
                for id, name, template_id in cursor:
                    arduinos.append(db_domain.Arduino(id, name, template_id))
        return arduinos

    def get_conditions(self) -> List[db_domain.Condition]:
        with closing(self.__create_connection()) as conn:
            with closing(conn.cursor(buffered=True)) as cursor:
                cursor.execute(
                    "SELECT id, type, operator, output_pin_id, status, from_time_hour, from_time_min, to_time_hour, "
                    "to_time_min FROM tbl_Condition")
                conditions = []
                for id, type, operator, output_pin_id, status, from_time_hour, from_time_min, to_time_hour, to_time_min in cursor:
                    with closing(conn.cursor(buffered=True)) as condition_cursor:
                        condition_cursor.execute("SELECT Condition_Child FROM tbl_Condition_Condition WHERE Condition_Parent=%s",
                                                 (id,))
                        condition_condition = []
                        for Condition_Child in condition_cursor:
                            condition_condition.append(Condition_Child[0])

                        if (from_time_hour is not None and from_time_min is not None and to_time_hour is not None and to_time_min is not None):
                            from_time = time(from_time_hour, from_time_min)
                            to_time = time(to_time_hour, to_time_min)
                        else:
                            from_time = None
                            to_time = None
                        conditions.append(
                            db_domain.Condition(id, type, operator, condition_condition, output_pin_id, status, from_time, to_time))

        return conditions

    def get_notifications(self) -> List[db_domain.Notification]:
        return None

    def get_triggers(self) -> List[db_domain.Trigger]:
        with closing(self.__create_connection()) as conn:
            with closing(conn.cursor(buffered=True)) as cursor:
                cursor.execute("SELECT id, trigger_type, seconds_down, time_between_tap FROM tbl_Trigger")
                triggers = []
                for id, trigger_type, seconds_down, time_between_tap in cursor:
                    triggers.append(db_domain.Trigger(id, trigger_type, seconds_down, time_between_tap))
        return triggers

    def get_input_pins(self) -> List[db_domain.InputPin]:
        with closing(self.__create_connection()) as conn:
            with closing(conn.cursor(buffered=True)) as cursor:
                cursor.execute("SELECT id, number, parent_id FROM tbl_InputPin")
                input_pins = []
                for id, number, parent_id in cursor:
                    with closing(conn.cursor(buffered=True)) as input_pins_cursor:
                        input_pins_cursor.execute("SELECT Action_ID FROM tbl_InputPin_Action WHERE InputPin_ID=%s", (id,))
                        input_pin_action = []
                        for Action_ID in input_pins_cursor:
                            input_pin_action.append(Action_ID[0])
                        input_pins.append(db_domain.InputPin(id, number, input_pin_action, parent_id))
        return input_pins

    def get_output_pins(self) -> List[db_domain.OutputPin]:
        with closing(self.__create_connection()) as conn:
            with closing(conn.cursor(buffered=True)) as cursor:
                cursor.execute("SELECT id, number, parent_id FROM tbl_OutputPin")
                output_pins = []
                for id, number, parent_id in cursor:
                    output_pins.append(db_domain.OutputPin(id, number, parent_id))
        return output_pins

    def get_actions(self) -> List[db_domain.Action]:
        with closing(self.__create_connection()) as conn:
            with closing(conn.cursor(buffered=True)) as cursor:
                cursor.execute("SELECT id, action_type, trigger_id, delay, timer, condition_id, master_id FROM tbl_Action")
                actions = []
                for id, action_type, trigger_id, delay, timer, condition_id, master_id in cursor:
                    with closing(conn.cursor(buffered=True)) as action_cursor:
                        action_cursor.execute("SELECT OutputPin_ID FROM tbl_Action_OutputPin WHERE Action_ID=%s", (id,))
                        output_pin_ids = []
                        for OutputPin_ID in action_cursor:
                            output_pin_ids.append(OutputPin_ID[0])
                        actions.append(
                            db_domain.Action(id, action_type, trigger_id, None, delay, timer, output_pin_ids, condition_id, master_id))
                            #TODO: ADD notification to the database

        return actions

    def __create_connection(self):
        return mariadb.connect(host=self.ip, port=self.port, user=self.username, password=self.password,
                               database=self.database)


def get_dummy_db() -> DbBase:
    """Returns a dummy database"""
    return DummyDb()


def get_maria_db() -> DbBase:
    """Returns an instance connecting to a maria database"""
    return MariaDB(databaseConfig['ip'], int(databaseConfig['port']), databaseConfig['username'],
                   databaseConfig['password'], databaseConfig['database'])
