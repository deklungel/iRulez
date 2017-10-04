import unittest
import src.irulez.domain as domain
import src.communication.mqtt_sender as mqtt_sender


class TestConvertIndividualPinsToCompleteArray(unittest.TestCase):
    def test_with_single_pin(self):
        # Setup
        individual_pins = [1]
        array_length = 5

        # Execute
        result = mqtt_sender.convert_individual_pins_to_complete_array(individual_pins, array_length)

        # Validate
        self.assertEqual([False, True, False, False, False], result)

    def test_with_multiple_pins(self):
        # Setup
        individual_pins = [1, 3]
        array_length = 5

        # Execute
        result = mqtt_sender.convert_individual_pins_to_complete_array(individual_pins, array_length)

        # Validate
        self.assertEqual([False, True, False, True, False], result)


class TestConvertIndividualPinsDictToCompleteArrayDict(unittest.TestCase):
    def setUp(self):
        self.name = "testArduino"
        arduino = domain.Arduino(self.name, 5, 5)
        output_pins = []
        for x in range(0, arduino.number_of_output_pins):
            output_pins.append([])
            output_pins[x] = domain.OutputPin(x, arduino.name)
        arduino.set_output_pins(output_pins)

        button_pins = []
        for x in range(0, arduino.number_of_button_pins):
            button_pins.append([])
            button_pins[x] = domain.ButtonPin(x, [], False)
        arduino.set_button_pins(button_pins)

        self.arduinos = {arduino.name: arduino}

        self.mqtt_sender = mqtt_sender.MqttSender(None, self.arduinos)

    def test_with_all_false_output_pins_in_arduino_and_all_pins_set_relatively(self):
        arduino_name = self.name
        pins_to_switch_on = {arduino_name: [0, 3, 4]}
        pins_to_switch_off = {arduino_name: [1, 2]}
        result_pins_on = {}
        result_pins_off = {}
        self.mqtt_sender.convert_individual_pins_dict_to_complete_array_dict(pins_to_switch_on, result_pins_on)
        self.mqtt_sender.convert_individual_pins_dict_to_complete_array_dict(pins_to_switch_off, result_pins_off)

        self.assertEqual([True, False, False, True, True], result_pins_on[arduino_name])
        self.assertEqual([False, True, True, False, False], result_pins_off[arduino_name])

    def test_with_all_false_output_pins_in_arduino_and_single_pin_on_relatively(self):
        arduino_name = self.name
        pins_to_switch_on = {arduino_name: [0]}
        result_pins_on = {}
        self.mqtt_sender.convert_individual_pins_dict_to_complete_array_dict(pins_to_switch_on, result_pins_on)

        self.assertEqual([True, False, False, False, False], result_pins_on[arduino_name])

    def test_with_output_pins_in_arduino_true_and_different_pin_on_relatively(self):
        arduino_name = self.name
        # Create individual pins
        pins_to_switch_on = {arduino_name: [0]}
        result_pins_on = {}
        self.mqtt_sender.convert_individual_pins_dict_to_complete_array_dict(pins_to_switch_on, result_pins_on)

        self.assertEqual([True, False, False, False, False], result_pins_on[arduino_name])

