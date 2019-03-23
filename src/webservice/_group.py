from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from src.webservice.base import Base

db = SQLAlchemy()
Base.query = db.session.query_property()


class Group(Base):
    __tablename__ = 'tbl_Groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    users = db.relationship("User")

    @staticmethod
    def get_all_groups():

        groups = Group.query.join(Group.users).all()
        output = []

        for group in groups:
            users = []
            for user in group.users:
                users.append(user.email)
            group_data = {'id': group.id, 'name': group.name, 'users': users}
            output.append(group_data)
        db.session.commit()
        return jsonify({'response': output})

    @staticmethod
    def create_new_group(request):
        data = request.get_json()

        new_group = Group(name=data["name"])
        db.session.add(new_group)
        db.session.commit()

        return jsonify({'result': 'User has been created'})

    @staticmethod
    def update_group(request):
        data = request.get_json()
        group = db.session.query(Group).filter_by(id=data['id']).first()
        if 'name' in data:
            group.email = data['name']
        db.session.commit()

        return jsonify({'result': 'User has been changed'})

    @staticmethod
    def delete_group(request):
        data = request.get_json()
        groups = db.session.query(Group).filter(Group.id.in_(data['id'])).all()
        for group in groups:
            db.session.delete(group)
        db.session.commit()

        return jsonify({'result': 'Group has been deleted'})

    @staticmethod
    def get_menu_fields_groups():
        groups = db.session.query(Group).all()
        output = []
        for group in groups:
            output.append({'id': group.id, 'name': group.name})
        db.session.close()
        return jsonify({'response': output})
