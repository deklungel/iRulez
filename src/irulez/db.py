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

        # Initialize an arduino with those relay_pins
        arduino = domain.Arduino("DEMO", 16, 16)

        # Create array of relay_pins with a variable number of pins.
        relay_pins = []
        for x in range(0, arduino.number_of_relay_pins):
            relay_pins.append([])
            relay_pins[x] = domain.OutputPin(x, arduino.name)

        arduino.set_relay_pins(relay_pins)

        # Create 2 actions.
        # Action 1 execute immediately, pins 0 and 10 ON
        # Action 2 execute immediately, pins 2, 5 and 9 OFF
        # Action 3 execute immediately, ping 7,9,10 TOGGLE

        action1 = domain.OnAction(domain.ImmediatelyActionTrigger(), 0,
                                [arduino.relay_pins[0], arduino.relay_pins[10]],
                                domain.MailNotification("Laurentmichel@me.com", True), None)
        action2 = domain.OffAction(domain.ImmediatelyActionTrigger(), 0,
                                [arduino.relay_pins[2], arduino.relay_pins[5], arduino.relay_pins[9]],
                                domain.TelegramNotification("azerty", True), None)

        action3 = domain.OffAction(domain.ImmediatelyActionTrigger(), domain.ActionType.TOGGLE, 0,
                                [arduino.relay_pins[8], arduino.relay_pins[9], arduino.relay_pins[10]],
                                domain.TelegramNotification("azerty", True), arduino.relay_pins[8])

        # Create array of button pins with a variable number of pins.
        button_pins = []
        for x in range(0, arduino.number_of_button_pins):
            button_pins.append([])
            button_pins[x] = domain.ButtonPin(x, [], False)

        button_pins[5].set_button_pin_actions([action1, action2])
        button_pins[10].set_button_pin_actions([action3])
        arduino.set_button_pins(button_pins)

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
