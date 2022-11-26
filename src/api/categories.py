from flask import request, jsonify, url_for, abort
from src import db
from src.api import bp
from src.api.errors import bad_request
from src.api.auth import token_auth, basic_auth

from src.models import User, Category

@bp.route('/categories', methods = ['POST'])
def created_category():
    data = request.get_json() or {}
    c = Category()
    if 'name' in data and data['name']!=c.name and c.query.filter_by(name=data['name']).first():
        return bad_request('Please use a different name')
    c.from_dict(data)
    db.session.add(c)
    db.session.commit()
    response = jsonify(c.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_plat', id=c.id)
    return response

@bp.route('/categories', methods = ['GET'])
def get_categories():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Category.to_collection_dict(Category.query, page, per_page, 'api.get_categories')
    return jsonify(data),201

@bp.route('/categories/<int:id>', methods = ['PUT'])
def update_category(id):
    data = request.get_json() or {}
    c = Category.query.get_or_404(id)
    if 'name' in data and data['name']==c.name:
        return bad_request('Please use a different name')
    c.from_dict(data, True)
    db.session.commit()
    response = jsonify(c.to_dict())
    response.message = 'Updating category'
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_category', id=c.id)
    return response

@bp.route('/categories/<int:id>', methods = ['GET'])
def get_category(id):
    c = Category.query.get(id)
    if c is None:
        return bad_request("User doesn't in database!")
    return jsonify(c.to_dict()), 201

@bp.route('/categories/<int:id>', methods = ['DELETE'])
def delete_category(id):
    c = Category.query.get(id) 
    if c is None:
        return bad_request("This category doesn't in database at id: "+str(id)+" !")
    db.session.delete(c)
    db.session.commit()
    return jsonify({
        "message": "The category is deleting with successfull"
    }), 201

