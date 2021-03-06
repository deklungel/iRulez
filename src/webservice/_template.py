from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Template(Base):
    __tablename__ = 'tbl_Template'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    nb_input_pins = db.Column(db.Integer)
    nb_output_pins = db.Column(db.Integer)

    @staticmethod
    def get_menu_fields_templates():
        rows = db.session.query(Template).all()
        output = []
        for row in rows:
            output.append({'id': row.id, 'name': row.name})
        db.session.close()
        return jsonify({'response': output})
