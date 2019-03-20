from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Action(Base):
    __tablename__ = 'tbl_Action'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    users = db.relationship("Input", secondary="tbl_InputPin_Action")

    @staticmethod
    def get_inputs(actionId):
        actions = db.session.query(Action).filter(Action.id.in_(actionId)).all()
        db.session.close()
        return actions
