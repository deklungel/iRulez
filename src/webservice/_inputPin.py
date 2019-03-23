from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from src.webservice.base import Base
from src.webservice._action import Action
db = SQLAlchemy()
Base.query = db.session.query_property()


class Input(Base):
    __tablename__ = 'tbl_InputPin'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer())
    name = db.Column(db.String(50))
    parent_id = db.Column(db.Integer, db.ForeignKey('tbl_Arduino.id'))
    parent = db.relationship('Device')
    time_between_clicks = db.Column(db.Float(50))
    actions = db.relationship("Action", secondary="tbl_InputPin_Action")

    @staticmethod
    def get_all_inputs():

        inputs = Input.query.outerjoin(Input.actions).all()
        output = []

        for input in inputs:
            actions = []
            actions_id = []
            for action in input.actions:
                actions.append(action.name)
                actions_id.append(action.id)
            input_data = {'id': input.id, 'name': input.name, 'device_name': input.parent.name, 'actions_id': actions_id,
                          'number': input.number, 'time_between_clicks': input.time_between_clicks, 'actions': actions}
            output.append(input_data)
        db.session.commit()
        return jsonify({'response': output})

    @staticmethod
    def update_input(request):
        data = request.get_json()
        input = db.session.query(Input).filter_by(id=data['id']).first()
        if 'name' in data:
            input.name = data['name']
        if 'time_between_clicks' in data:
            input.time_between_clicks = data['time_between_clicks']
        if 'actions_id':
            actions = Action.get_actions(data['actions_id'])
            input.actions = actions
        db.session.commit()

        return jsonify({'result': 'User has been changed'})

