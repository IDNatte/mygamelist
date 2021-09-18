from flask import Blueprint
from flask import jsonify

admin = Blueprint('admin_endpoint', __name__)


@admin.route('/api/admin')
def admin_index():
    return jsonify({'test': 'test'})
