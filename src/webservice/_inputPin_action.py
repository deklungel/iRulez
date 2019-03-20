from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class InputPin_Action(Base):
    __tablename__ = 'tbl_InputPin_Action'
    id = db.Column(db.Integer, primary_key=True)
    InputPin_ID = db.Column(db.Integer, db.ForeignKey('tbl_InputPin.id'))
    Action_ID = db.Column(db.Integer, db.ForeignKey('tbl_Action.id'))
