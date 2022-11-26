from flask import request, jsonify, url_for, abort
from src import db
from src.api import bp
from src.api.errors import bad_request
from src.api.auth import token_auth, basic_auth
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.models import User, UserRoles

# registed user 
@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods = ['PUT'])
# @token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {} 
    if 'username' in data and data['username']!=user.username and User.query.filter_by(username=data['username']).first():
        return bad_request('Please use a different username')
    if 'email' in data and data['email']!=user.email and  User.query.filter_by(email=data['email']).first():
        return bad_request('Please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

# get one user 
@bp.route('/users/<int:id>', methods = ['GET'])
# @token_auth.login_required
def get_user(id):
    user = User.query.get(id)
    print(user)
    if user is None:
        return bad_request("User doesn't in database!")
    return jsonify(user.to_dict())

# deleted user 
@bp.route('/users/<int:id>', methods = ['DELETE'])
def delete_user(id):
    user = User.query.get(id) 
    if user is None:
        return bad_request("User doesn't in database!")
    db.session.delete(user)
    db.session.commit()
    return jsonify({
        "message": "The user is deleting with successfull"
    })

# get all users 
@bp.route('/users', methods=['GET'])
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users/profile', methods = ['POST', 'GET'])
@token_auth.login_required
def profile():
    user_token = basic_auth.current_user()    
    user = User.query.get_or_404(user_token.id)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'POST':
        # print(request.get_json())
        data = request.get_json() or {}
        if 'image' in data:
            user.upload(data['image'])
        user.from_dict(data, new_user=False)
        # db.session.commit()
        # user_up = user.to_dict()
        # user_up['message'] = "User is updated with successfull"
        return jsonify({'user_up':''})
