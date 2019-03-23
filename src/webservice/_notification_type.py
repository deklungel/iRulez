from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Notification_Type(Base):
    __tablename__ = 'tbl_Notification_Type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
