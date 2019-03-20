from flask import jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from src.webservice.base import Base


db = SQLAlchemy()
Base.query = db.session.query_property()


class User(Base):
    __tablename__ = 'tbl_Users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    refresh_token = db.Column(db.String(50))
    group_id = db.Column(db.Integer, db.ForeignKey('tbl_Groups.id'))
    group = db.relationship('Group')


    @staticmethod
    def login(request):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response("Bad Request", 401)

        user = User.query.filter_by(email=auth.username).first()

        if not user:
            return make_response("Could not verify", 401)

        if check_password_hash(user.password, auth.password):
            user.refresh_token = str(uuid.uuid4())
            db.session.commit()

            private_key = open('private.key').read()
            token = jwt.encode({'public_id': user.public_id, 'username': user.email,
                                'admin': user.admin, 'refreshToken': user.refresh_token,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                               private_key, algorithm='RS256').decode('utf-8')
            return jsonify({'token': token})

        return make_response("Could not verify", 401)


    @staticmethod
    def refresh_login(request):
        data = request.get_json()
        if not data['refreshToken']:
            return jsonify({"message": "You are not allowed to perform this action"}), 401
        user = User.query.filter_by(refresh_token=data['refreshToken']).first()
        if not user:
            return jsonify({"message": "You are not allowed to perform this action"}), 401

        user.refresh_token = str(uuid.uuid4())
        db.session.commit()

        private_key = open('private.key').read()
        token = jwt.encode({'public_id': user.public_id, 'username': user.email,
                            'admin': user.admin, 'refreshToken': user.refresh_token,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                           private_key, algorithm='RS256').decode('utf-8')
        return jsonify({'token': token})


    @staticmethod
    def get_all_users():
        users = User.query.all()
        output = []

        for user in users:
            user_data = {'id': user.public_id, 'email': user.email}
            if user.admin:
                user_data['role'] = 'admin'
            else:
                user_data['role'] = 'user'
            user_data['group_name'] = user.group.name
            user_data['group_id'] = user.group_id
            output.append(user_data)

        return jsonify({'response': output})

    @staticmethod
    def create_new_user(request):
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        admin = False
        if data["role"] == "admin":
            admin = True
        new_user = User(public_id=str(uuid.uuid4()), email=data["email"], group_id=data["group_id"],
                        password=hashed_password, admin=admin)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'result': 'User has been created'})

    @staticmethod
    def update_user(request):
        data = request.get_json()
        user = db.session.query(User).filter_by(public_id=data['id']).first()
        if 'email' in data:
            user.email = data['email']
        if 'group_id' in data:
            user.group_id = data['group_id']
        if 'password' in data:
            user.password = generate_password_hash(data['password'], method='sha256')

        db.session.commit()
        return jsonify({'result': 'User has been changed'})

    @staticmethod
    def delete_user(request):
        data = request.get_json()
        users = db.session.query(User).filter(User.public_id.in_(data['id'])).all()
        for user in users:
            db.session.delete(user)
        db.session.commit()

        return jsonify({'result': 'User has been deleted'})
