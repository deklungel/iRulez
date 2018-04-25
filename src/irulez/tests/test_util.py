import unittest
import src.irulez.util as util
import src.irulez.constants as constants


class TestIsArduinoTopic(unittest.TestCase):
    def test_empty_string(self) -> None:
        result = util.is_arduino_topic('')
        self.assertFalse(result)

    def test_valid_string(self) -> None:
        result = util.is_arduino_topic(constants.arduinoTopic + '/')
        self.assertTrue(result)

    def test_invalid_string(self) -> None:
        result = util.is_arduino_topic('blabla ')
        self.assertFalse(result)

    def test_not_startswith_arduino_topic(self) -> None:
        result = util.is_arduino_topic('blabla ' + constants.arduinoTopic)
        self.assertFalse(result)


class TestIsArduinoActionTopic(unittest.TestCase):
    def test_empty_string(self) -> None:
        self.assertFalse(util.is_arduino_action_topic(''))


class TestGetFromJsonObject(unittest.TestCase):
    def test_get_int(self) -> None:
        json_object = util.serialize_json({"key": 1})
        deserialized = util.deserialize_json(json_object)
        result = util.get_int_from_json_object(deserialized, "key")
        self.assertEqual(1, result)

    def test_get_bool(self) -> None:
        json_object = util.serialize_json({"key": True})
        deserialized = util.deserialize_json(json_object)
        result = util.get_int_from_json_object(deserialized, "key")
        self.assertEqual(True, result)


if __name__ == '__main__':
    unittest.main(verbosity=2)
