import configparser
from pathlib import Path


class Configuration:
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read(str(Path(__file__).resolve().parents[0].resolve()) + '/config.ini')


    def get_config(self, section: str) -> {}:
        if section in self.config:
            return self.config[section]
        return None

    def get_mqtt_config(self) -> {}:
        return self.get_config('MQTT')

    def get_database_config(self) -> {}:
        return self.get_config('Database')

    # noinspection PyPep8Naming
    def authenticate_SMTP_config(self) -> {}:
        return self.get_config('authenticate_SMTP')

    def get_service_client_config(self) -> {}:
        return self.get_config('output_status_client')

    def get_service_server_config(self) -> {}:
        return self.get_config('output_status_server')

    def get_webserver_config(self) -> {}:
        return self.get_config('webserver')

