from flask import jsonify, make_response, Response
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Output(Base):
    __tablename__ = 'tbl_OutputPin'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer())
    name = db.Column(db.String(50))
    parent_id = db.Column(db.Integer, db.ForeignKey('tbl_Arduino.id'))
    parent = db.relationship('Device')
    type = db.Column(db.Integer(), db.ForeignKey('tbl_OutputPin_Type.id'))
    type_name = db.relationship('OutputPin_Type')
    actions = db.relationship("Action", secondary="tbl_Action_OutputPin")

    @staticmethod
    def get_all_outputs():

        output_pins = Output.query.outerjoin(Output.actions).all()
        output = []

        for outputPin in output_pins:
            output.append({'id': outputPin.id, 'name': outputPin.name, 'number': outputPin.number,
                          'type_name': outputPin.type_name.name, 'type': outputPin.type, 'device_name': outputPin.parent.name})

        db.session.commit()
        return jsonify({'response': output})

    @staticmethod
    def update_output(request):
        data = request.get_json()
        output = db.session.query(Output).filter_by(id=data['id']).first()
        if 'name' in data:
            output.name = data['name']
        if 'type' in data:
            if len(output.actions) == 0:
                output.type = data['type']
            else:
                db.session.commit()
                return "error", "500 Output pin is used in actions"
        db.session.commit()
        return jsonify({'result': 'Output pin has been changed'})

    @staticmethod
    def get_outputs(outputID):
        output = db.session.query(Output).filter(Output.id.in_(outputID)).all()
        db.session.commit()
        return output

    @staticmethod
    def get_menu_fields_outputs():
        outputs = db.session.query(Output).all()
        output = []
        for row in outputs:
            output.append({'id': row.id, 'name': row.name})
        db.session.close()
        return jsonify({'response': output})
