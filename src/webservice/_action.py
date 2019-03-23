from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base
from src.webservice._notification import Notification
from src.webservice._outputPin import Output

db = SQLAlchemy()
Base.query = db.session.query_property()


class Action(Base):
    __tablename__ = 'tbl_Action'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    action_type = db.Column(db.Integer, db.ForeignKey('tbl_Action_Type.id'))
    type = db.relationship('Action_Type', foreign_keys=[action_type])
    trigger_id = db.Column(db.Integer, db.ForeignKey('tbl_Trigger.id'))
    trigger = db.relationship('Trigger', foreign_keys=[trigger_id])
    delay = db.Column(db.Integer)
    timer = db.Column(db.Integer)
    master_id = db.Column(db.Integer, db.ForeignKey('tbl_OutputPin.id'))
    master = db.relationship('Output', foreign_keys=[master_id])
    condition_id = db.Column(db.Integer, db.ForeignKey('tbl_Condition.id'))
    condition = db.relationship('Condition', foreign_keys=[condition_id])
    click_number = db.Column(db.Integer)
    dim_master_id = db.Column(db.Integer, db.ForeignKey('tbl_OutputPin.id'))
    dim_master = db.relationship('Output', foreign_keys=[dim_master_id])
    dimmer_speed = db.Column(db.Integer)
    dimmer_light_value = db.Column(db.Integer)
    cancel_on_button_release = db.Column(db.Boolean)

    outputs = db.relationship("Output", secondary="tbl_Action_OutputPin")
    inputs = db.relationship("Input", secondary="tbl_InputPin_Action")
    notifications = db.relationship("Notification", secondary="tbl_Action_Notification")

    @staticmethod
    def get_all_relais_actions():

        relais_actions = db.session.query(Action).filter(Action.action_type <= 4).all()
        output = []

        for relais_action in relais_actions:
            output_pin_id = []
            output_pin_name = []
            for output_pin in relais_action.outputs:
                output_pin_id.append(output_pin.id)
                output_pin_name.append(output_pin.name)
            notification_id = []
            notification_name = []
            for notification in relais_action.notifications:
                notification_id.append(notification.id)
                notification_name.append(notification.name)
            master_name = ''
            if relais_action.master:
                master_name = relais_action.master.name
            condition_name = ''
            if relais_action.condition:
                condition_name = relais_action.condition.name
            output.append({'id' : relais_action.id, 'name': relais_action.name,
                           'action_type_name': relais_action.type.name,
                          'action_type': relais_action.action_type, 'trigger': relais_action.trigger_id,
                           'trigger_name': relais_action.trigger.name, 'delay': relais_action.delay,
                           'timer': relais_action.timer, 'master_id': relais_action.master_id, 'master': master_name,
                           'condition_id': relais_action.condition_id, 'condition': condition_name,
                           'click_number': relais_action.click_number, 'outputs_id': output_pin_id,
                           'outputs': output_pin_name, 'notifications_id': notification_id,
                           'notifications': notification_name})
        return jsonify({'response': output})


    @staticmethod
    def new_action(request):
        data = request.get_json()
        if data['master_id'] == '':
            data['master_id'] = None
        if data['delay'] == '':
            data['delay'] = 0
        if data['timer'] == '':
            data['timer'] = 0
        if data['condition_id'] == '':
            data['condition_id'] = None

        new_action = Action(name=data["name"], action_type=data['action_type'], trigger_id=data['trigger'],
                            delay=data['delay'], timer=data['timer'], master_id=data['master_id'],
                            condition_id=data['condition_id'], click_number=data['click_number'],
                            outputs=Output.get_outputs(data['outputs_id']),
                            notifications=Notification.get_notifications(data['notifications_id']))

        db.session.add(new_action)
        db.session.commit()

        return jsonify({'result': 'User has been created'})

    @staticmethod
    def update_action(request):
        data = request.get_json()
        action = db.session.query(Action).filter_by(id=data['id']).first()
        if 'name' in data:
            action.name = data['name']
        if 'action_type' in data:
            action.action_type = data['action_type']
        if 'trigger' in data:
            action.trigger = data['trigger']
        if 'delay' in data:
            if data['delay'] == '':
                data['delay'] = 0
            action.delay = data['delay']
        if 'timer' in data:
            if data['timer'] == '':
                data['timer'] = 0
            action.timer = data['timer']
        if 'master_id' in data:
            if data['master_id'] == '':
                data['master_id'] = None
            action.master_id = data['master_id']
        if 'condition_id' in data:
            if data['condition_id'] == '':
                data['condition_id'] = None
            action.condition_id = data['condition_id']
        if 'click_number' in data:
            action.click_number = data['click_number']
        if 'notifications_id' in data:
            notifications = Notification.get_notifications(data['notifications_id'])
            action.notifications = notifications
        if 'outputs_id' in data:
            print(data['outputs_id'])
            outputs = Output.get_outputs(data['outputs_id'])
            action.outputs = outputs
        db.session.commit()

        return jsonify({'result': 'Action has been changed'})

    @staticmethod
    def delete_action(request):
        data = request.get_json()
        actions = db.session.query(Action).filter(Action.id.in_(data['id'])).all()
        for action in actions:
            db.session.delete(action)
        db.session.commit()

        return jsonify({'result': 'Action has been deleted'})

    @staticmethod
    def get_all_dimmer_actions():

        dimmer_actions = db.session.query(Action).filter(Action.action_type > 4).all()
        output = []

        for dimmer_action in dimmer_actions:
            output_pin_id = []
            output_pin_name = []
            for output_pin in dimmer_action.outputs:
                output_pin_id.append(output_pin.id)
                output_pin_name.append(output_pin.name)
            notification_id = []
            notification_name = []
            for notification in dimmer_action.notifications:
                notification_id.append(notification.id)
                notification_name.append(notification.name)
            master_name = ''
            if dimmer_action.dim_master:
                master_name = dimmer_action.dim_master.name
            condition_name = ''
            if dimmer_action.condition:
                condition_name = dimmer_action.condition.name
            output.append({'id': dimmer_action.id, 'name': dimmer_action.name,
                           'action_type_name': dimmer_action.type.name,
                           'action_type': dimmer_action.action_type, 'trigger': dimmer_action.trigger_id,
                           'trigger_name': dimmer_action.trigger.name, 'delay': dimmer_action.delay,
                           'timer': dimmer_action.timer, 'master_id': dimmer_action.dim_master_id, 'master': master_name,
                           'condition_id': dimmer_action.condition_id, 'condition': condition_name,
                           'click_number': dimmer_action.click_number, 'outputs_id': output_pin_id,
                           'outputs': output_pin_name, 'notifications_id': notification_id,
                           'notifications': notification_name})
        return jsonify({'response': output})

    @staticmethod
    def get_actions(actionId):
        actions = db.session.query(Action).filter(Action.id.in_(actionId)).all()
        db.session.close()
        return actions

    @staticmethod
    def get_menu_fields_actions():
        actions = db.session.query(Action).all()
        output = []
        for action in actions:
            output.append({'id': action.id, 'name': action.name})
        db.session.close()
        return jsonify({'response': output})
