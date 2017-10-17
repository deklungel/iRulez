import src.irulez.log as log
import src.timer.timer_domain as timer_domain
import src.irulez.domain as domain
from threading import Timer
import src.irulez.constants as constants
import uuid
import src.timer.mqtt_sender as mqtt_sender
import json


logger = log.get_logger('timer_processor')


class TimerProcessor:
    def __init__(self,sender: mqtt_sender.MqttSender):
        self.PythonTimers = {} # key=guid (id from the timer), values=Python buildin timer (fires action) object= Treading.Timer
        self.ActionTimers = {} # key=guid (id from the timer), values=object conains data for execution of the timer object=timer_domain.Timer
        self.sender = sender

    def process_timer_action(self, payload: str):

        json_object = json.loads(payload)

        # Before creating a new Timer we check if the pins exist in a other Timer.
        # If this is the case we remove the pins from the other timer.
        self.check_output_pin(json_object)

        # create an id for new timer
        timer_id = uuid.uuid4()

        # create Timer object
        self.ActionTimers[timer_id] = timer_domain.RelativeActionTimer(json_object['name'], json_object['topic'], json_object['on'], json_object['off'])
        t = Timer(int(json_object['delay']), self.execute_timer_action, args=(timer_id,))
        t.start()
        self.PythonTimers[timer_id] = t
        logger.info(f"Timer created with '{timer_id}'.")

    def execute_timer_action(self, timer_id):
        logger.info(f"Timer with timer_id '{timer_id}' has finished. Start executing actions.")
        action_timer = self.ActionTimers.get(timer_id, None)
        if action_timer is None:
            # Unknown Action
            logger.info(f"Could not find Action timer with timer_id '{timer_id}'.")
            return

        self.sender.publish_relative_action(domain.IndividualAction(action_timer.name, constants.arduinoTopic + '/' +
                                                                 constants.actionTopic + '/' +
                                                                 constants.relative, 0,
                                                                 action_timer.output_pins_on,
                                                                 action_timer.output_pins_off))

        # After the timer is executed we remove the timers from ActionTimers and PythonTimers
        logger.debug(f"Delete executed timers")
        del(self.ActionTimers[timer_id])
        del (self.PythonTimers[timer_id])

    def check_output_pin(self, json_object: []):
        for timer_id in self.ActionTimers:
            if self.ActionTimers[timer_id].name == json_object['name']:
                self.ActionTimers[timer_id].check_pins(json_object)
        self.check_empty_timer()

    def check_empty_timer(self):
        to_be_delete = []
        for timer_id in self.ActionTimers:
            if self.ActionTimers[timer_id].check_empty_timer():
                python_timer = self.PythonTimers.get(timer_id, None)
                if python_timer is None:
                    logger.info(f"Could not find Python timer with timer_id '{timer_id}'.")
                logger.info(f"Cancel timer")
                python_timer.cancel()
                to_be_delete.append(timer_id)

        for timer_id in to_be_delete:
            del (self.ActionTimers[timer_id])
            del (self.PythonTimers[timer_id])
            logger.info(f"Delete ActionTimer and PythonTimers with timer_id '{timer_id}'.")





