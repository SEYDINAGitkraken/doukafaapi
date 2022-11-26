from flask import jsonify, request, url_for
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from src.models import User
from src.api.errors import error_response, bad_request
from flask_login import current_user, login_user
from src import db
from src.api import bp

token_auth = HTTPTokenAuth()
basic_auth = HTTPBasicAuth()


@basic_auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username='admin').first()
    if user and user.check_password(password='admin'):
        return user

@basic_auth.error_handler
def basic_auth_error(status):
    return error_response(status)

@token_auth.verify_token
def verify_token(token='KsfKLU9qoqRThLycCQzAqkc5DVFFiw9y'):
    token = 'KsfKLU9qoqRThLycCQzAqkc5DVFFiw9y'
    return User.check_token(token) if token else None

@token_auth.error_handler
def token_auth_error(status):
    return error_response(status)

# login 
@bp.route('/login', methods=['POST', 'GET'])
def login():
    data = request.get_json() or {} 
    if 'username' not in data or 'password' not in data:
        return bad_request('must include username and password fields')
    user = User.query.filter_by(username=data['username']).first()
    if user is None or not user.check_password(data['password']):
        return bad_request('Invalid username or password')
    login_user(user)
    access_token = user.get_token()
    user_login = user.to_dict()
    user_login['access_token'] = access_token

    print(basic_auth.current_user())
    return jsonify(user_login), 201

# register 
@bp.route('/register', methods = ['POST'])
def register():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('the user exists, change the username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('the user exists, change the eamil adress')
    user = User()
    user.set_password(data['password'])
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response
