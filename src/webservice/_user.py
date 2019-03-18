from flask import jsonify
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)

    @staticmethod
    def get_all_users():

        users = User.query.all()
        output = []

        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['admin'] = user.admin
            output.append(user_data)

        return jsonify({'result': output})

    @staticmethod
    def create_new_user(request):
        data = request.get_json()
        print(data['name'])
        return ''

