from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Action_Type(Base):
    __tablename__ = 'tbl_Action_Type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    @staticmethod
    def get_menu_fields_action_type_relais():
        action_types = db.session.query(Action_Type).filter(Action_Type.id <= 4).all()
        output = []
        for action_type in action_types:
            output.append({'id': action_type.id, 'name': action_type.name})
        db.session.close()
        return jsonify({'response': output})

    @staticmethod
    def get_menu_fields_action_type_dimmer():
        action_types = db.session.query(Action_Type).filter(Action_Type.id <= 4).all()
        output = []
        for action_type in action_types:
            output.append({'id': action_type.id, 'name': action_type.name})
        db.session.close()
        return jsonify({'response': output})