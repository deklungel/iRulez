from flask import jsonify, make_response
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Group(db.Model):
    __tablename__ = 'tbl_Groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
