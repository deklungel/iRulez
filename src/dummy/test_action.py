import lib.paho.mqtt.publish as publish
import time
import src.irulez.constants as constants
import src.irulez.util as util
import src.irulez.configuration as configuration
import src.irulez.log as logger

log = logger.get_logger("test_action")

# Connect
config = configuration.Configuration()
mqttConfig = config.get_mqtt_config()
databaseConfig = config.get_database_config()

arduino = input("Arduino name? <[DEMO]|virtual_IO_Board> ")
number_of_pin = input("Number of pins? <[16]|20> ")
pin = input("Pin [10]")
button_type = input("C: [CLICK], L: LOW, H: HIGH M : Multi-click ")
if button_type == '':
    button_type = 'C'

if arduino == '':
    arduino = "DEMO"
if number_of_pin == '':
    number_of_pin = 16
if pin == '':
    pin = 10


pin_states = [0] * int(number_of_pin)
pin_states_Release = [0] * int(number_of_pin)


pin_states[int(pin)] = 1

payload = util.convert_array_to_hex(pin_states)
payload_release = util.convert_array_to_hex(pin_states_Release)

if button_type == 'C':
    log.info(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic + "/" + payload)
    publish.single(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic, payload,
                   auth={'username': mqttConfig['username'], 'password': mqttConfig['password']},
                   hostname=mqttConfig['ip'],
                   port=int(mqttConfig['port']), retain=False)
    time.sleep(1)
    log.info(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic + "/" + payload_release)
    publish.single(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic, payload_release,
                   auth={'username': mqttConfig['username'], 'password': mqttConfig['password']},
                   hostname=mqttConfig['ip'],
                   port=int(mqttConfig['port']), retain=False)

if button_type == 'L':
    lowtimer = input("Low for how many sec, 0 for forever? [0] ")
    if lowtimer == '':
        lowtimer = 0
    log.info(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic + "/" + payload)
    publish.single(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic, payload,
                   auth={'username': mqttConfig['username'], 'password': mqttConfig['password']},
                   hostname=mqttConfig['ip'],
                   port=int(mqttConfig['port']), retain=False)
    time.sleep(int(lowtimer))
    log.info(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic + "/" + payload_release)
    publish.single(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic, payload_release,
                   auth={'username': mqttConfig['username'], 'password': mqttConfig['password']},
                   hostname=mqttConfig['ip'],
                   port=int(mqttConfig['port']), retain=False)

if button_type == 'H':
    log.info(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic + "/" + payload_release)
    publish.single(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic, payload_release,
                   auth={'username': mqttConfig['username'], 'password': mqttConfig['password']},
                   hostname=mqttConfig['ip'],
                   port=int(mqttConfig['port']), retain=False)

if button_type == 'M':
    clicks = input("How many clicks do you want to trigger? [3] ")
    if clicks == '':
        clicks = 3
    for x in range(0, int(clicks)):
        log.info(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic + "/" + payload)
        publish.single(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic, payload,
                       auth={'username': mqttConfig['username'], 'password': mqttConfig['password']},
                       hostname=mqttConfig['ip'],
                       port=int(mqttConfig['port']), retain=False)
        log.info(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic + "/" + payload_release)
        publish.single(constants.arduinoTopic + "/" + arduino + "/" + constants.buttonTopic, payload_release,
                       auth={'username': mqttConfig['username'], 'password': mqttConfig['password']},
                       hostname=mqttConfig['ip'],
                       port=int(mqttConfig['port']), retain=False)
