import src.irulez.log as log
import src.timer.timer_domain as timer_domain
from threading import Timer
import src.irulez.constants as constants
import uuid
import src.timer.mqtt_sender as mqtt_sender
import src.irulez.util as util

logger = log.get_logger('timer_processor')


class TimerProcessor:
    def __init__(self, sender: mqtt_sender.MqttSender):
        # key=guid (id from the timer), values=Python built-in timer (fires action) object= Treading.Timer
        self.PythonTimers = {}
        # key=guid (id from the timer), values=object contains data for execution of the timer object=timer_domain.Timer
        self.ActionTimers = {}
        self.__default_timers = {}
        self.sender = sender

    def process_default_timer_request(self, payload: str):
        json_object = util.deserialize_json(payload)

        topic = util.get_str_from_json_object(json_object, 'topic')
        delay = util.get_int_from_json_object(json_object, 'delay')
        payload = json_object['payload']

        # create an id for new timer
        timer_id = uuid.uuid4()
        self.__default_timers[timer_id] = timer_domain.DefaultTimer(topic, payload)
        t = Timer(int(delay)/100, self.__execute_default_timer, args=(timer_id,))
        t.start()
        self.PythonTimers[timer_id] = t
        logger.info(f"Timer created with '{timer_id}'.")

    def __execute_default_timer(self, timer_id) -> None:
        logger.info(f"Default timer with timer_id '{timer_id}' has finished. Start executing actions.")
        timer_to_execute = self.__default_timers.get(timer_id, None)
        if timer_to_execute is None:
            # Unknown Action
            logger.info(f"Could not find default timer with timer_id '{timer_id}'.")
            return

        # After the timer is executed we remove the timers from ActionTimers and PythonTimers
        logger.debug(f"Delete executed timers")
        del (self.__default_timers[timer_id])
        del (self.PythonTimers[timer_id])

        if not isinstance(timer_to_execute, timer_domain.DefaultTimer):
            logger.error(f"Found timer in __default_timers with id '{timer_id}', "
                         f"but it wasn't a DefaultTimer ({type(timer_to_execute)})")
            return

        self.sender.publish_default_action(timer_to_execute.topic, timer_to_execute.payload)

    def process_timer_action_request(self, payload: str):

        json_object = util.deserialize_json(payload)

        # Before creating a new Timer we check if the pins exist in a other Timer.
        # If this is the case we remove the pins from the other timer.
        self.check_output_pin(json_object)

        # create an id for new timer
        timer_id = uuid.uuid4()

        # create Timer object
        self.ActionTimers[timer_id] = timer_domain.RelativeActionTimer(json_object['name'],
                                                                       json_object['topic'],
                                                                       json_object['on'],
                                                                       json_object['off'])
        t = Timer(int(json_object['delay']), self.__execute_timer_action, args=(timer_id,))
        t.start()
        self.PythonTimers[timer_id] = t
        logger.info(f"Timer created with '{timer_id}'.")

    def __execute_timer_action(self, timer_id) -> None:
        logger.info(f"Timer with timer_id '{timer_id}' has finished. Start executing actions.")
        action_timer = self.ActionTimers.get(timer_id, None)
        if action_timer is None:
            # Unknown Action
            logger.info(f"Could not find Action timer with timer_id '{timer_id}'.")
            return

        self.sender.publish_relative_action(timer_domain.IndividualAction(action_timer.name,
                                                                          constants.iRulezTopic + '/' +
                                                                          constants.actionTopic + '/' +
                                                                          constants.relativeTopic, 0,
                                                                          action_timer.output_pins_on,
                                                                          action_timer.output_pins_off))

        # After the timer is executed we remove the timers from ActionTimers and PythonTimers
        logger.debug(f"Delete executed timers")
        del (self.ActionTimers[timer_id])
        del (self.PythonTimers[timer_id])

    def check_output_pin(self, json_object: []):
        for timer_id in self.ActionTimers:
            if self.ActionTimers[timer_id].name == json_object['name']:
                self.ActionTimers[timer_id].check_pins(json_object)
        self.__check_empty_timer()

    def __check_empty_timer(self) -> None:
        to_be_delete = []
        for timer_id in self.ActionTimers:
            if self.ActionTimers[timer_id].check_empty_timer():
                python_timer = self.PythonTimers.get(timer_id, None)
                if python_timer is None:
                    logger.info(f"Could not find Python timer with timer_id '{timer_id}'.")
                logger.info(f"Cancel timer 1")
                python_timer.cancel()
                to_be_delete.append(timer_id)

        for timer_id in to_be_delete:
            del (self.ActionTimers[timer_id])
            del (self.PythonTimers[timer_id])
            logger.info(f"Delete ActionTimer and PythonTimers with timer_id '{timer_id}'.")
