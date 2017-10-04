import configparser

class configuration():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

    def GetConfig(self,section: str) -> {}:
        print(self.config.sections())
        if section in self.config:
            return self.config['MQTT']
        return None
