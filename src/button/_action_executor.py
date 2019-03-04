import src.button._mqtt_sender as mqtt_sender
import src.button._domain as domain
from typing import Dict, List
import src.irulez.log as log
from datetime import datetime
import src.output_status.ServiceClient as ServiceClient
import src.irulez.util as util

logger = log.get_logger('button_processor')


class ActionExecutor:
    """
    Contains logic for executing all kinds of actions
    """

    def __init__(self, sender: mqtt_sender.MqttSender, status_service: ServiceClient.StatusServiceClient):
        self.__sender = sender
        self.__status_service = status_service

    def check_condition(self, condition: domain.Condition):
        if condition is None:
            return True
        if condition.condition_type == domain.ConditionType.TIME and isinstance(condition, domain.TimeCondition):
            return condition.from_time <= datetime.now().time() <= condition.to_time
        elif condition.condition_type == domain.ConditionType.OUTPUT_PIN and \
                isinstance(condition, domain.OutputPinCondition):
            return condition.status == self.__status_service.get_arduino_pin_status(condition.output_pin.parent,
                                                                                    condition.output_pin.number)
        elif condition.condition_type == domain.ConditionType.LIST and isinstance(condition, domain.ConditionList):
            for condition in condition.conditions:
                if condition.operator == domain.Operator.AND:
                    for condition in condition.conditions:
                        if not self.check_condition(condition):
                            return False
                    return True
                    # Otherwise it's OR
                for condition in condition.conditions:
                    if self.check_condition(condition):
                        return True
                    return False
        else:
            logger.warning("Condition not caught")
            return False

    def process_notification(self, action: domain.Action):
        if action.notifications is None:
            return
        for notification in action.notifications:
            topic = notification.get_topic_name()
            payload = notification.get_payload()
            self.__sender.publish_notification(topic, payload)

    def execute_action(self,
                       action: domain.Action,
                       pins_to_switch: Dict[str, List[domain.IndividualAction]],
                       pins_to_dim: Dict[str, List[domain.IndividualDimAction]],
                       last_light_values_to_update: Dict[int, int]) -> None:
        """ Performs the given action by manipulating the given dictionaries with pins. """
        if self.check_condition(action.get_condition()):
            logger.info(f"Process action with type '{action.action_type}'")
            if isinstance(action, domain.OnAction):
                action.perform_action(pins_to_switch)
            elif isinstance(action, domain.OffAction):
                action.perform_action(pins_to_switch)
            elif isinstance(action, domain.ToggleAction):
                master = self.__status_service.get_arduino_pin_status(action.master.parent, action.master.number)
                action.perform_action(pins_to_switch, master)
            elif isinstance(action, domain.OnDimmerAction):
                action.perform_action(pins_to_dim)
            elif isinstance(action, domain.OffDimmerAction):
                action.perform_action(pins_to_dim)
            elif isinstance(action, domain.ToggleDimmerAction):
                master_json = self.__status_service.get_arduino_dim_pin_status(action.master.parent,
                                                                               action.master.number)
                # JSON contains 'state' and 'direction'
                master = util.deserialize_json(master_json)
                state = util.get_int_from_json_object(master, 'state')
                direction = util.get_str_from_json_object(master, 'direction')
                last_light_value_optional = None
                if action.master_dim_id is not None:
                    last_light_value_optional = self.__status_service.get_dimmer_light_value(action.master.parent,
                                                                                             action.master_dim_id)
                last_light_value = 100
                if last_light_value_optional is not None:
                    last_light_value = last_light_value_optional
                action.perform_action(pins_to_dim, last_light_values_to_update, state, direction, last_light_value)
            else:
                logger.error(f"Undefined action of type '{action.action_type}' ({type(action)})")
        else:
            logger.info(f"Condition not met")

    def execute_actions(self, actions: List[domain.Action], button: domain.ButtonPin, arduino_name: str):
        pins_to_switch = {}
        pins_to_dim = {}
        last_light_values_to_update = {}

        logger.debug(f"Publish immediate actions")
        for action in actions:
            self.execute_action(action, pins_to_switch, pins_to_dim, last_light_values_to_update)

        self.__sender.publish_last_light_values(last_light_values_to_update)
        self.__sender.publish_relative_action(pins_to_switch)
        self.__sender.publish_dimmer_module_action(pins_to_dim, arduino_name, button.number)
