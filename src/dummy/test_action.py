import lib.paho.mqtt.publish as publish
import src.irulez.db
import src.irulez.constants as constants
import src.irulez.util as util
import src.irulez.configuration as configuration
import lib.mysql.connector as mariadb

# Connect
config = configuration.Configuration()
mqttConfig = config.get_mqtt_config()
databaseConfig = config.get_database_config()

# Get database, dummy for now
database = src.irulez.db.get_MarinaDB_db()

Test = database.get_templates()


arduino = input("Arduino name? <DEMO|virtual_IO_Board> ")
number_of_pin = input("Numver of pins? <16|20>")
pin = input("Pin ")
button_action = input("B: Button , A: action ")

pin_states = [0] * int(number_of_pin)

if (pin != ""):
    list = pin.split('|');
    for relay in list:
        pin_states[int(relay)] = 1

payload = util.convert_array_to_hex(pin_states)

if (button_action == "A"):
    print(constants.arduinoTopic + "/" + arduino + "/" + constants.actionTopic + "/" + payload)

    publish.single(constants.arduinoTopic + "/" + arduino + "/" + constants.actionTopic, payload,
                   auth={'username': mqttConfig['username'], 'password': mqttConfig['password']},
                   hostname=mqttConfig['ip'],
                   port=mqttConfig['port'], retain=False)

elif (button_action == "B"):
    print(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic + "/" + payload)

    publish.single(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic, payload,
                   auth={'username': mqttConfig['username'], 'password': mqttConfig['password']},
                   hostname=mqttConfig['ip'],
                   port=mqttConfig['port'], retain=False)
