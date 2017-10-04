import src.irulez.domain as domain
from abc import ABC, abstractmethod
import src.irulez.constants as constants
from datetime import time


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

        # Initialize an arduino with those output_pins
        arduino = domain.Arduino("DEMO", 16, 16)

        # Create array of output_pins with a variable number of pins.
        output_pins = []
        for x in range(0, arduino.number_of_output_pins):
            output_pins.append([])
            output_pins[x] = domain.OutputPin(x, arduino.name)

        arduino.set_output_pins(output_pins)

        # create Time condition
        condition1 = domain.TimeCondition(time(9, 0), time(12, 00))
        condition2 = domain.TimeCondition(time(18, 0), time(23, 59))
        # create OR Condition
        condition_list1 = domain.ConditionList(domain.Operator.OR, [condition1, condition2])

        # create output condition
        condition3 = domain.OutputPinCondition(arduino.output_pins[15], True)

        # create AND condition
        condition_list2 = domain.ConditionList(domain.Operator.AND, [condition_list1, condition3])

        # Create 3 actions.
        # Action 1 execute immediately, pins 0 and 10 ON
        # Action 2 execute immediately, pins 2, 5 and 9 OFF
        # Action 3 execute immediately, ping 7,9,10 TOGGLE

        action1 = domain.OnAction(domain.ImmediatelyActionTrigger(), 0,
                                  [arduino.output_pins[0], arduino.output_pins[10]],
                                  domain.MailNotification("Laurentmichel@me.com", True), condition_list2)
        action2 = domain.OffAction(domain.ImmediatelyActionTrigger(), 0,
                                   [arduino.output_pins[2], arduino.output_pins[5], arduino.output_pins[9]],
                                   domain.TelegramNotification("azerty", True), None)
        action3 = domain.ToggleAction(domain.ImmediatelyActionTrigger(), 0,
                                      [arduino.output_pins[8], arduino.output_pins[9], arduino.output_pins[10]],
                                      domain.TelegramNotification("azerty", True), arduino.output_pins[8], None)

        # Create array of button pins with a variable number of pins.
        button_pins = []
        for x in range(0, arduino.number_of_button_pins):
            button_pins.append([])
            button_pins[x] = domain.ButtonPin(x, [], False)

        button_pins[5].set_button_pin_actions([action1, action2])
        button_pins[10].set_button_pin_actions([action3])
        arduino.set_button_pins(button_pins)

        # Create 2th arduino (Virtual)
        virtual_arduino = domain.Arduino(constants.virtual_IO_board_name, constants.virtual_IO_board_outputs,
                                         constants.virtual_IO_board_buttons)
        # Create array of output_pins with a variable number of pins.
        output_pins = []
        for x in range(0, virtual_arduino.number_of_output_pins):
            output_pins.append([])
            output_pins[x] = domain.OutputPin(x, virtual_arduino.name)

            virtual_arduino.set_output_pins(output_pins)

        action1 = domain.OnAction(domain.ImmediatelyActionTrigger(), 0,
                                  [virtual_arduino.output_pins[0]],
                                  domain.MailNotification("Laurentmichel@me.com", True), None)
        action2 = domain.OffAction(domain.ImmediatelyActionTrigger(), 0,
                                   [virtual_arduino.output_pins[0], virtual_arduino.output_pins[4]],
                                   domain.MailNotification("Laurentmichel@me.com", True), None)

        # Create array of button pins with a variable number of pins.
        button_pins = []
        for x in range(0, virtual_arduino.number_of_button_pins):
            button_pins.append([])
            button_pins[x] = domain.ButtonPin(x, [], False)

        button_pins[5].set_button_pin_actions([action1])
        button_pins[10].set_button_pin_actions([action2])
        virtual_arduino.set_button_pins(button_pins)

        # Initialize the dictionary of arduinos (contains only 1 for now)
        # Key is name of the arduino
        # return domain.ArduinoConfig([arduino, virtual_arduino])
        return domain.ArduinoConfig([virtual_arduino])

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
