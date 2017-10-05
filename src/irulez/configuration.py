import configparser


class Configuration:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('../irulez/config.ini')

    def get_config(self, section: str) -> {}:
        if section in self.config:
            return self.config[section]
        return None

    def get_mqtt_config(self) -> {}:
        return self.get_config('MQTT')

    def get_database_config(self) -> {}:
        return self.get_config('Database')
