from typing import Dict, List, Optional
import src.button.domain as domain
import src.irulez.db as db
import src.irulez.db_domain as db_domain
import src.irulez.log as log

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
        logger.debug('Retrieving input pins from database')
        input_pins = self.db.get_input_pins()
        logger.debug('Retrieving output pins from database')
        output_pins = self.db.get_output_pins()
        logger.debug('Retrieving actions from database')
        actions = self.db.get_actions()
        logger.debug('Retrieving triggers from database')
        triggers = self.db.get_triggers()
        logger.debug('Retrieving conditions from database')
        conditions = self.db.get_conditions()
        logger.debug('Retrieving notifications from database')
        notifications = self.db.get_notifications()

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

        # Create conditions
        # We have to do these all at once since they reference each other
        created_conditions = self.__create_conditions(conditions, created_output_pins)

        # Create notification
        created_notifications = dict()
        if notifications is not None:
            for notification in notifications:
                created_notifications[notification.id] = self.__create_notification(notification)

        # Create triggers
        created_triggers = dict()
        for trigger in triggers:
            created_triggers[trigger.id] = self.__create_trigger(trigger)

        # Create actions
        created_actions = dict()
        for action in actions:
            created_action = self.__create_action(action, created_triggers, created_output_pins, created_conditions,
                                                  created_notifications)
            if created_action is not None:
                created_actions[action.id] = created_action

        # Create input pins
        created_input_pins = dict()
        for input_pin in input_pins:
            created_input_pin = self.__create_input_pin_and_add_to_arduino(input_pin, created_arduinos, created_actions)
            if created_input_pin is not None:
                created_input_pins[input_pin.id] = created_input_pin

        # Verify all input pins are set in arduinos
        for arduino in created_arduinos.values():
            self.__validate_input_pins(arduino)

        return domain.ArduinoConfig(list(created_arduinos.values()))

    def __create_trigger(self, trigger: db_domain.Trigger) -> domain.ActionTrigger:
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

    def __create_notification(self, notification: db_domain.Notification) -> domain.Notification:
        if notification.notification_type == 1:
            return domain.MailNotification(notification.message, notification.subject,
                                           notification.emails, notification.enabled)
        if notification.notification_type == 2:
            return domain.TelegramNotification(notification.message, notification.tokens, notification.enabled)

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

        return domain.Arduino(arduino.name, nb_output, nb_input)

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

    def __create_conditions(self, conditions: List[db_domain.Condition],
                            output_pins: Dict[int, domain.OutputPin]) -> Dict[int, domain.Condition]:

        to_process = []
        to_process.extend(conditions)
        previous_length = len(to_process) + 1  # Trigger first loop always
        to_return = dict()

        # While we have items to process and we aren't stuck with the same amount as previous loop
        while 0 < len(to_process) < previous_length:
            logger.debug("__create_conditions: previous_length: " + str(previous_length))
            logger.debug("__create_conditions: len(to_process): " + str(len(to_process)))
            # Update length to process
            previous_length = len(to_process)
            unprocessed = []

            for condition in to_process:
                if condition.type == domain.ConditionType.TIME:
                    to_return[condition.id] = domain.TimeCondition(condition.from_time, condition.to_time)
                elif condition.type == domain.ConditionType.OUTPUT_PIN:
                    created_cond = self.__create_output_pin_condition(condition, output_pins)
                    if created_cond is not None:
                        to_return[condition.id] = created_cond
                else:
                    # ConditionList
                    created_cond = self.__create_condition_list(condition, to_return)
                    if created_cond is not None:
                        to_return[condition.id] = created_cond
                    else:
                        unprocessed.append(condition)

            to_process = unprocessed
            # logger.debug("end __create_conditions")
        return to_return

    def __create_output_pin_condition(self, condition: db_domain.Condition,
                                      output_pins: Dict[int, domain.OutputPin]) -> Optional[domain.Condition]:
        output_pin = output_pins.get(condition.output_pin_id, None)
        if output_pin is None:
            logger.warning(f'Output pin {condition.output_pin_id} was not found for condition {condition.id}')
            return None
        return domain.OutputPinCondition(output_pin, bool(condition.status))

    def __create_condition_list(self, condition: db_domain.Condition,
                                conditions: Dict[int, domain.Condition]) -> Optional[domain.Condition]:
        # Try to retrieve all required conditions
        conditions_in_list = []

        for condition_id in condition.condition_ids:
            retrieved_condition = conditions.get(condition_id, None)
            if retrieved_condition is None:
                # Not all required conditions are created yet, wait for next loop
                return None
            conditions_in_list.append(retrieved_condition)

        # All conditions found, hurray
        return domain.ConditionList(domain.Operator(condition.operator), conditions_in_list)

    def __create_action(self, action: db_domain.Action, triggers: Dict[int, domain.ActionTrigger],
                        output_pins: Dict[int, domain.OutputPin],
                        conditions: Dict[int, domain.Condition], notifications: Dict[int, domain.Notification]) \
            -> Optional[domain.Action]:
        # Try to retrieve the action trigger
        trigger = triggers.get(action.trigger_id, None)
        if trigger is None:
            logger.warning(f'The trigger {action.trigger_id} could not be found for action {action.id}')
            return None

        # Try to retrieve all output pins
        pins_of_action = []
        for pin_id in action.output_pin_ids:
            pin = output_pins.get(pin_id, None)
            if pin is None:
                logger.warning(f'The output pin {pin_id} could not be found for action {action.id}')
                return None
            pins_of_action.append(pin)

        # Try to retrieve the condition, which is optional
        condition = None
        if action.condition_id is not None:
            condition = conditions.get(action.condition_id, None)
            if condition is None:
                logger.warning(f'The condition {action.condition_id} could not be found for action {action.id}')
                return None

        # Try to retrieve the notification, which is optional
        notification_of_action = []
        if action.notification_ids is not None:
            for notification in action.notification_ids:
                notification_of_action.append(notifications.get(notification))

        if action.action_type == 1:
            # Get master pin
            master_pin = output_pins.get(action.master_id, None)
            if master_pin is None:
                logger.warning(f'The master pin {action.master_id} could not be found for action {action.id}')
            return domain.ToggleAction(trigger, action.delay, pins_of_action, notification_of_action, master_pin,
                                       condition, action.click_number)
        if action.action_type == 2:
            return domain.OnAction(trigger, action.delay, action.timer, pins_of_action, notification_of_action,
                                   condition, action.click_number)
        if action.action_type == 3:
            return domain.OffAction(trigger, action.delay, action.timer, pins_of_action, notification_of_action,
                                    condition, action.click_number)

        # Other types not supported yet
        logger.error(f'Type {action.action_type} not supported yet')
        return None

    def __create_input_pin_and_add_to_arduino(self, input_pin: db_domain.InputPin, arduinos: Dict[int, domain.Arduino],
                                              actions: Dict[int, domain.Action]) -> Optional[domain.ButtonPin]:
        # Try get parent
        arduino = arduinos.get(input_pin.parent_id, None)
        if arduino is None:
            logger.warning(f'Arduino with id {input_pin.parent_id} not found. Not creating input pin {input_pin.id}')
            return None

        # Try get actions
        actions_of_button = []
        for action_id in input_pin.action_ids:
            act = actions.get(action_id, None)
            if act is None:
                logger.warning(f'Action with id {action_id} was not found for input pin {input_pin.id}')
                return None
            actions_of_button.append(act)

        to_return = domain.ButtonPin(input_pin.number, actions_of_button, input_pin.time_between_clicks)
        arduino.set_button_pin(to_return)
        return to_return

    def __validate_input_pins(self, arduino: domain.Arduino):
        for i in range(0, arduino.number_of_button_pins):
            pin = arduino.button_pins.get(i, None)
            if pin is None:
                logger.warning(f'Button pin {i} of arduino {arduino.name} was not set!')
