from typing import Dict, Optional

import src.output_status.db_domain as db_domain

import src.button.db as db
import src.irulez.log as log
import src.output_status.domain as domain

logger = log.get_logger('factory')


class ArduinoConfigFactory:
    def __init__(self, db: db.DbBase):
        self.db = db

    def create_arduino_config(self) -> domain.ArduinoConfig:
        # Retrieve the whole universe from the database
        logger.debug('Retrieving arduinos from database')
        arduinos = self.db.get_arduinos()
        logger.debug('Retrieving templates from database')
        templates = self.db.get_templates()
        logger.debug('Retrieving output pins from database')
        output_pins = self.db.get_output_pins()

        logger.info("Got all data from database")

        # Map templates
        mapped_templates = dict()
        for template in templates:
            mapped_templates[template.id] = template

        # Create arduinos
        created_arduinos = dict()
        for arduino in arduinos:
            created_arduinos[arduino.id] = self.__create_arduino(arduino, mapped_templates)

        # Create output pins
        created_output_pins = dict()
        for output_pin in output_pins:
            created_pin = self.__create_output_pin_and_add_to_arduino(output_pin, created_arduinos)
            if created_pin is not None:
                created_output_pins[output_pin.id] = created_pin

        # Verify all output pins are set in arduinos
        for arduino in created_arduinos.values():
            self.__validate_output_pins(arduino)


        return domain.ArduinoConfig(list(created_arduinos.values()))

    def __create_output_pin_and_add_to_arduino(self, output_pin: db_domain.OutputPin,
                                               arduinos: Dict[int, domain.Arduino]) -> Optional[domain.OutputPin]:
        arduino = arduinos.get(output_pin.parent_id, None)
        if arduino is None:
            logger.warning(f'Arduino with id {output_pin.parent_id} was not found. Not creating pin {output_pin.id}')
            return None

        to_return = domain.OutputPin(output_pin.number, arduino.name)
        arduino.set_output_pin(to_return)
        return to_return

    def __validate_output_pins(self, arduino: domain.Arduino):
        for i in range(0, arduino.number_of_output_pins):
            pin = arduino.output_pins.get(i, None)
            if pin is None:
                logger.warning(f'Output pin {i} of arduino {arduino.name} was not set!')

    def __create_arduino(self, arduino: db_domain.Arduino, templates: Dict[int, db_domain.Template]) -> domain.Arduino:
        template = templates.get(arduino.template_id, None)
        nb_input = 16
        nb_output = 16
        if template is None:
            logger.warning(
                f'Template {arduino.template_id} was not found in the templates. '
                f'Fallback to default values for arduino {arduino.id}')
        else:
            nb_input = template.nb_input_pins
            nb_output = template.nb_output_pins

        return domain.Arduino(arduino.name, nb_output)


