from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Device(Base):
    __tablename__ = 'tbl_Arduino'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    mac = db.Column(db.String(17))
    sn = db.Column(db.String(10))
    template_id = db.Column(db.Integer, db.ForeignKey('tbl_Template.id'))
    template = db.relationship('Template')
    version = db.Column(db.String(17))
    mac = db.Column(db.String(17))
    ping = db.Column(db.Boolean)
    mqtt = db.Column(db.Boolean)

    @staticmethod
    def get_all_devices():

        devices = Device.query.all()
        output = []
        for device in devices:
            group_data = {'id': device.id, 'name': device.name,
                          'mac': device.mac, 'template_name': device.template.name,
                          'sn': device.sn, 'version': device.version, 'ping': device.ping,
                          'mqtt': device.mqtt}
            output.append(group_data)
        db.session.commit()
        return jsonify({'response': output})

    @staticmethod
    def create_new_device(request):
        data = request.get_json()

        new_device = Device(name=data["name"], mac=data["mac"], sn=data['sn'], template_id=data['template_id'])
        db.session.add(new_device)
        db.session.commit()
        return jsonify({'result': 'Device has been created'})

    @staticmethod
    def update_device(request):
        data = request.get_json()
        device = db.session.query(Device).filter_by(id=data['id']).first()
        if 'mac' in data:
            device.mac = data['mac']
        if 'sn' in data:
            device.sn = data['sn']
        db.session.commit()
        return jsonify({'result': 'Device has been changed'})

    @staticmethod
    def delete_device(request):
        data = request.get_json()
        devices = db.session.query(Device).filter(Device.id.in_(data['id'])).all()
        for device in devices:
            db.session.delete(device)
        db.session.commit()

        return jsonify({'result': 'Device has been deleted'})
