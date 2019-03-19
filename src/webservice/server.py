from flask import Flask, request, jsonify
from src.webservice._user import User
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:irulez4database@10.0.50.50/iRulez'

db = SQLAlchemy(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'token is missing!'}, 401)

        try:
            public_key = open('public.key').read()
            data = jwt.decode(token, public_key, algorithms=['RS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalide'})

        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/api/login', methods=['POST'])
def login_route():
    return User.login(request)


@app.route('/api/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def user_route(current_user):
    if not current_user.admin:
        return jsonify({"message": "You are not allowed to perform this action"})

    if request.method == 'GET':
        return User.get_all_users()
    elif request.method == 'POST':
        return User.create_new_user(request)
    elif request.method == 'PUT':
        return User.update_user(request)
    elif request.method == 'DELETE':
        return User.delete_user(request)


if __name__ == '__main__':
    app.run('127.0.0.1', 5000)
