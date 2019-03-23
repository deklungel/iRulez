from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Trigger(Base):
    __tablename__ = 'tbl_Trigger'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    trigger_type = db.Column(db.Integer(), db.ForeignKey('tbl_Trigger_Type.id'))
    seconds_down = db.Column(db.Integer)

    @staticmethod
    def get_menu_fields_triggers():
        triggers = db.session.query(Trigger).all()
        output = []
        for trigger in triggers:
            output.append({'id': trigger.id, 'name': trigger.name})
        db.session.close()
        return jsonify({'response': output})
