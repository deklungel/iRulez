from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Notification(Base):
    __tablename__ = 'tbl_Notification'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    notification_type = db.Column(db.Integer, db.ForeignKey('tbl_Notification_Type.id'))
    message = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    enabled = db.Column(db.Boolean)

    @staticmethod
    def get_notifications(notificationId):
        notification = db.session.query(Notification).filter(Notification.id.in_(notificationId)).all()
        db.session.commit()
        return notification

    @staticmethod
    def get_menu_fields_notifications():
        rows = db.session.query(Notification).all()
        output = []
        for row in rows:
            output.append({'id': row.id, 'name': row.name})
        db.session.close()
        return jsonify({'response': output})
