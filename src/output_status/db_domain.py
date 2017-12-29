
class Arduino:
    def __init__(self, id: int, name: str, template_id: int):
        self.id = id
        self.name = name
        self.template_id = template_id


class Template:
    def __init__(self, id: int, name: str, nb_input_pins: int, nb_output_pins: int):
        self.id = id
        self.name = name
        self.nb_input_pins = nb_input_pins
        self.nb_output_pins = nb_output_pins


class OutputPin:
    def __init__(self, id: int, number: int, parent_id: int):
        self.parent_id = parent_id
        self.number = number
        self.id = id
