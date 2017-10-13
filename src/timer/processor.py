import src.irulez.log as log
import src.timer.timer_domain as timerDomain
import src.irulez.domain as Domain
from threading import Timer
import src.irulez.util as util
import uuid
import src.communication.mqtt_sender as mqtt_sender
import json


logger = log.get_logger('timer_processor')



class TimerProcessor:
    def __init__(self,sender: mqtt_sender.MqttSender, arduinos: {}):
        self.arduinos = arduinos
        self.PythonTimers = {}
        self.ActionTimers = {}
        self.sender = sender

    def ProcessTimerAction(self, name: str, payload: str):
        jsonObject = json.loads(payload)

        self.CheckOutputPin(name, jsonObject)


        guid = uuid.uuid4()

        self.ActionTimers[guid] = timerDomain.Timer(name, jsonObject['on'],jsonObject['off'])
        t = Timer(int(jsonObject['delay']), self.ExecuteTimerAction, args=(guid,))
        t.start()
        self.PythonTimers[guid] = t
        logger.info(f"Timer created with '{guid}'.")

    def ExecuteTimerAction(self, guid):
        logger.info(f"Timer with guid '{guid}' has finished. Start executing actions.")
        actionTimer = self.ActionTimers.get(guid, None)
        if actionTimer is None:
            # Unknown arduino
            logger.info(f"Could not find Action timer with guid '{guid}'.")
            return
        pins_to_switch_on = {}
        pins_to_switch_off = {}

        pins_to_switch_on[actionTimer.name] = [Domain.IndividualAction(0,actionTimer.output_pins_on)]
        pins_to_switch_off[actionTimer.name] = [Domain.IndividualAction(0, actionTimer.output_pins_off)]

        self.sender.send_relative_update(pins_to_switch_on, pins_to_switch_off)

        logger.debug(f"Delete executed timers")
        del(self.ActionTimers[guid])
        del (self.PythonTimers[guid])


    def CheckOutputPin(self, parrentname: str, jsonobject: []):
        for name in  self.ActionTimers:
            if self.ActionTimers[name].name == parrentname:
                self.ActionTimers[name].checkPins(jsonobject)
        self.checkEmptyTimer()

    def checkEmptyTimer(self):
        to_be_delete = []
        for guid in self.ActionTimers:
            if(self.ActionTimers[guid].checkEmptyTimer()):
                pythontimer = self.PythonTimers.get(guid, None)
                if pythontimer is None:
                    logger.info(f"Could not find Pyton timer with guid '{guid}'.")
                logger.info(f"Cancel timer")
                pythontimer.cancel()
                to_be_delete.append(guid)

        for guid in to_be_delete:
            del (self.ActionTimers[guid])
            del (self.PythonTimers[guid])
            logger.info(f"Delete ActionTimer and PythonTimers with guid '{guid}'.")





