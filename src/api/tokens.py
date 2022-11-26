from flask import jsonify
from src import db
from src.api import bp
from src.api.auth import basic_auth
from src.api.errors import bad_request
from flask_login import current_user


@bp.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = basic_auth.current_user().get_token()
    db.session.commit()
    return jsonify({'token': token})
