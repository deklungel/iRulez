from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
from flask_cors import CORS
from src.webservice._user import User
from src.webservice._group import Group

app = Flask(__name__)
cors = CORS(app, resources={"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:irulez4database@10.0.50.50/iRulez'
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 50
app.config['SQLALCHEMY_POOL_SIZE'] = 20
db = SQLAlchemy(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        print(auth_header)
        if not auth_header:
            return jsonify({'statusText': 'token is missing!'}), 401

        token = auth_header.split(" ")[1]
        if not token:
            return jsonify({'statusText': 'token is missing!'}), 401
        try:
            public_key = open('public.key').read()
            data = jwt.decode(token, public_key, algorithms=['RS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'statusText': 'Token is invalide'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/api/login', methods=['POST'])
def login_route():
    return User.login(request)


@app.route('/api/refresh_login', methods=['POST'])
def login_refresh_route():
    return User.refresh_login(request)


@app.route('/api/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def user_route(current_user):
    if not current_user.admin:
        return jsonify({"message": "You are not allowed to perform this action"}), 401

    if request.method == 'GET':
        return User.get_all_users()
    elif request.method == 'POST':
        return User.create_new_user(request)
    elif request.method == 'PUT':
        return User.update_user(request)
    elif request.method == 'DELETE':
        return User.delete_user(request)


@app.route('/api/groups', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def group_route(current_user):
    if not current_user.admin:
        return jsonify({"message": "You are not allowed to perform this action"})

    if request.method == 'GET':
        return Group.get_all_groups()
    elif request.method == 'POST':
        return Group.create_new_group(request)
    elif request.method == 'PUT':
        return Group.update_group(request)
    elif request.method == 'DELETE':
        return Group.delete_group(request)


if __name__ == '__main__':
    app.run('0.0.0.0', 3004)
