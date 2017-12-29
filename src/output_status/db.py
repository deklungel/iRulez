import src.output_status.db_domain as db_domain
import lib.mysql.connector as mariadb
from abc import ABC, abstractmethod
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
    def get_output_pins(self) -> List[db_domain.OutputPin]:
        """Retrieves the output pins as they are known in the database"""
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

    def get_output_pins(self) -> List[db_domain.OutputPin]:
        with closing(self.__create_connection()) as conn:
            with closing(conn.cursor(buffered=True)) as cursor:
                cursor.execute("SELECT id, number, parent_id FROM tbl_OutputPin")
                output_pins = []
                for id, number, parent_id in cursor:
                    output_pins.append(db_domain.OutputPin(id, number, parent_id))
                return output_pins

    def __create_connection(self) -> None:
        return mariadb.connect(host=self.ip, port=self.port, user=self.username, password=self.password,
                               database=self.database)


def get_dummy_db() -> DbBase:
    """Returns a dummy database"""
    return DummyDb()


def get_maria_db() -> DbBase:
    """Returns an instance connecting to a maria database"""
    return MariaDB(databaseConfig['ip'], int(databaseConfig['port']), databaseConfig['username'],
                   databaseConfig['password'], databaseConfig['database'])
