import src.irulez.db as db
import src.irulez.db_domain as db_domain
import src.irulez.domain as domain
import src.irulez.log as log

logger = log.get_logger('factory')

class ArduinoConfigFactory:
    def __init__(self, db: db.DbBase):
        self.db = db

    def create_arduino_config(self):
        # Retrieve the whole universe from the database
        arduinos = self.db.get_arduinos()
        templates = self.db.get_templates()
        input_pins = self.db.get_input_pins()
        output_pins = self.db.get_output_pins()
        actions = self.db.get_actions()
        triggers = self.db.get_triggers()
        conditions = self.db.get_conditions()

        # Start creating simplest objects first: triggers
        created_triggers = {}
        for trig in triggers:
            if not trig is db_domain.Trigger:
                logger.warning('An element was found in the trigger list which was not a db_domain.Trigger!')
                continue
            created_triggers[trig]

    def create_trigger(self, trigger: db_domain.Trigger) -> domain.ActionTrigger:
        if trigger.trigger_type == 1:
            return domain.ImmediatelyActionTrigger()
        if trigger.trigger_type == 2:
            return domain.AfterReleaseActionTrigger()
        if trigger.trigger_type == 3:
            return domain.LongDownActionTrigger(trigger.seconds_down)
        if trigger.trigger_type == 4:
            return domain.DoubleTapActionTrigger(trigger.time_between_tap)
        if trigger.trigger_type == 5:
            return domain.TripleTapActionTrigger(trigger.time_between_tap)

