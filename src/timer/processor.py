import src.irulez.log as log
import src.irulez.timer_domain as timerDomain
from threading import Timer

logger = log.get_logger('absolute_update_processor')


class TimerProcessor:
    def __init__(self):
        self.timers = {}

    def ProcessTimerAction(self, name: str, payload: str):
        pass

    def CheckOutputPin(self, name: str, payload: str):
        pass
