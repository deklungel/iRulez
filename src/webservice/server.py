from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
from flask_cors import CORS

import src.irulez.log as log

from src.webservice._user import User
from src.webservice._group import Group
from src.webservice._device import Device
from src.webservice._inputPin import Input
from src.webservice._template import Template
from src.webservice._inputPin_action import InputPin_Action
from src.webservice._outputPin_action import OutputPin_Action
from src.webservice._action import Action
from src.webservice._outputPin import Output
from src.webservice._menu import Menu
from src.webservice._outputPinType import OutputPin_Type
from  src.webservice._action_notification import Notification_Action
from src.webservice._notification import Notification
from src.webservice._trigger import Trigger
from src.webservice._action_type import Action_Type
from src.webservice._condition import Condition
from src.webservice._notification_type import Notification_Type

logger = log.get_logger('webserver')

app = Flask(__name__)
CORS(app, resources={"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:irulez4database@10.0.50.50/iRulez'
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 50
app.config['SQLALCHEMY_POOL_SIZE'] = 20
db = SQLAlchemy(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logger.debug('Check for token')
        token = None
        auth_header = request.headers.get('Authorization')
        logger.debug(auth_header)
        if not auth_header:
            logger.debug('Authorization header not found')
            return jsonify({'statusText': 'token is missing!'}), 401

        token = auth_header.split(" ")[1]
        if not token:
            logger.debug('Token not found in Header')
            return jsonify({'statusText': 'token is missing!'}), 401
        try:
            public_key = open('public.key').read()
            data = jwt.decode(token, public_key, algorithms=['RS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
            if not current_user:
                logger.debug('No user found with public_id: ' + data['public_id'])
                return jsonify({'statusText': 'token is missing!'}), 401
        except:
            logger.error('Unable to decrypt token, token is invalide')
            return jsonify({'statusText': 'Token is invalide'}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@app.route('/api/login', methods=['POST'])
def login_route():
    logger.debug('login route')
    return User.login(request)


@app.route('/api/refresh_login', methods=['POST'])
def login_refresh_route():
    logger.debug('refresh login route')
    return User.refresh_login(request)


@app.route('/api/users', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def user_route(current_user):
    if not current_user.admin:
        logger.debug('No admin user')
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
    logger.debug('groups route. Method -> ' + request.method)
    if not current_user.admin:
        logger.debug('No admin user')
        return jsonify({"message": "You are not allowed to perform this action"}), 401

    if request.method == 'GET':
        return Group.get_all_groups()
    elif request.method == 'POST':
        return Group.create_new_group(request)
    elif request.method == 'PUT':
        return Group.update_group(request)
    elif request.method == 'DELETE':
        return Group.delete_group(request)


@app.route('/api/devices', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def device_route(current_user):
    logger.debug('devices route. Method -> ' + request.method)
    if not current_user.admin:
        logger.debug('No admin user')
        return jsonify({"message": "You are not allowed to perform this action"})

    if request.method == 'GET':
        return Device.get_all_devices()
    elif request.method == 'POST':
        return Device.create_new_device(request)
    elif request.method == 'PUT':
        return Device.update_device(request)
    elif request.method == 'DELETE':
        return Device.delete_device(request)


@app.route('/api/inputs', methods=['GET', 'PUT'])
@token_required
def input_route(current_user):
    logger.debug('inputs route. Method -> ' + request.method)
    if not current_user.admin:
        logger.debug('No admin user')
        return jsonify({"message": "You are not allowed to perform this action"})

    if request.method == 'GET':
        return Input.get_all_inputs()
    elif request.method == 'PUT':
        return Input.update_input(request)


@app.route('/api/outputs', methods=['GET', 'PUT'])
@token_required
def output_route(current_user):
    logger.debug('output route. Method -> ' + request.method)
    if not current_user.admin:
        logger.debug('No admin user')
        return jsonify({"message": "You are not allowed to perform this action"})

    if request.method == 'GET':
        return Output.get_all_outputs()
    elif request.method == 'PUT':
        return Output.update_output(request)


@app.route('/api/menus', methods=['GET', 'PUT', 'POST', 'DELETE'])
@token_required
def menu_route(current_user):
    logger.debug('menu route. Method -> ' + request.method)
    if not current_user.admin:
        logger.debug('No admin user')
        return jsonify({"message": "You are not allowed to perform this action"})

    if request.method == 'GET':
        return Menu.get_all_menus()
    elif request.method == 'POST':
        return Menu.create_new_menu(request)
    elif request.method == 'PUT':
        return Menu.update_menu(request)
    elif request.method == 'DELETE':
        return Menu.delete_menu(request)


@app.route('/api/actions/relais', methods=['GET', 'PUT', 'POST', 'DELETE'])
@token_required
def action_relais_route(current_user):
    logger.debug('relais action route. Method -> ' + request.method)
    if not current_user.admin:
        logger.debug('No admin user')
        return jsonify({"message": "You are not allowed to perform this action"})

    if request.method == 'GET':
        return Action.get_all_relais_actions()
    elif request.method == 'POST':
        return Action.new_action(request)
    elif request.method == 'PUT':
        return Action.update_action(request)
    elif request.method == 'DELETE':
        return Action.delete_action(request)


@app.route('/api/actions/dimmers', methods=['GET', 'PUT'])
@token_required
def action_dimmer_route(current_user):
    logger.debug('relais action route. Method -> ' + request.method)
    if not current_user.admin:
        logger.debug('No admin user')
        return jsonify({"message": "You are not allowed to perform this action"})

    if request.method == 'GET':
        return Action.get_all_dimmer_actions()


@app.route('/api/field/<field>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@token_required
def fields_route(current_user, field):
    logger.debug('field route. Method -> ' + request.method)
    if not current_user.admin:
        logger.debug('No admin user')
        return jsonify({"message": "You are not allowed to perform this action"})

    if field == 'actions':
        return Action.get_menu_fields_actions()
    if field == 'triggers':
        return Trigger.get_menu_fields_triggers()
    if field == 'groups':
        return Group.get_menu_fields_groups()
    if field == 'action_types_relais':
        return Action_Type.get_menu_fields_action_type_relais()
    if field == 'outputs':
        return Output.get_menu_fields_outputs()
    if field == 'notifications':
        return Notification.get_menu_fields_notifications()
    if field == 'conditions':
        return Condition.get_menu_fields_conditions()
    if field == 'templates':
        return Template.get_menu_fields_templates()
    if field == 'menus':
        return Menu.get_menu_fields_menus()
    if field == 'output_type':
        return OutputPin_Type.get_menu_fields_output_type()



    return jsonify({"message": "field not implemented"}), 501

if __name__ == '__main__':
    app.run('0.0.0.0', 3004)
