from flask import request, jsonify, url_for, abort
from src import db
from src.api import bp
from src.api.errors import bad_request
from src.api.auth import token_auth, basic_auth
from src.models import User, Plat


@bp.route('/plats', methods=['POST'])
def created_plat():
    data = request.get_json() or {}
    p = Plat()
    if 'name' in data and data['name']!=p.name and p.query.filter_by(name=data['name']).first():
        return bad_request('Please use a different name')
    p.from_dict(data)
    db.session.add(p)
    db.session.commit()
    response = jsonify(p.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_plat', id=p.id)
    return response

@bp.route('/plats', methods=['GET'])
def get_plats():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = Plat.to_collection_dict(Plat.query, page, per_page, 'api.get_plats')
    return jsonify(data),201

@bp.route('/plats/<int:id>', methods = ['PUT'])
def update_plat(id):
    p = Plat.query.get_or_404(id)
    data = request.get_json() or {} 
    if 'name' in data and data['name']==p.name:
        return bad_request('Please use a different name')
    p.from_dict(data, True)
    db.session.commit()
    response = jsonify(p.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_plat', id=p.id)
    return response

@bp.route('/plats/<int:id>', methods=['GET'])
def get_plat(id):
    p = Plat.query.get(id)
    if p is None:
        return bad_request("User doesn't in database!")
    return jsonify(p.to_dict()), 201

@bp.route('/plats/<int:id>', methods = ['DELETE'])
def delete_plat(id):
    p = Plat.query.get(id) 
    if p is None:
        return bad_request("This plat doesn't in database at id: "+str(id)+" !")
    db.session.delete(p)
    db.session.commit()
    return jsonify({
        "message": "The plat is deleting with successfull"
    }), 201

