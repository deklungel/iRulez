from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Condition(Base):
    __tablename__ = 'tbl_Condition'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    @staticmethod
    def get_menu_fields_conditions():
        rows = db.session.query(Condition).all()
        output = []
        for row in rows:
            output.append({'id': row.id, 'name': row.name})
        db.session.close()
        return jsonify({'response': output})
