from flask import Blueprint
from flask import jsonify

user = Blueprint('user_endpoint', __name__)


@user.route('/api/user')
def user_index():
    return jsonify({'test': 'test'})
