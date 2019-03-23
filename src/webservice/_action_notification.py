from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Notification_Action(Base):
    __tablename__ = 'tbl_Action_Notification'
    id = db.Column(db.Integer, primary_key=True)
    Notification_id = db.Column(db.Integer, db.ForeignKey('tbl_Notification.id'))
    Action_ID = db.Column(db.Integer, db.ForeignKey('tbl_Action.id'))
