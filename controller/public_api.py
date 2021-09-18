from flask import Blueprint
from flask import jsonify

public = Blueprint('public_endpoint', __name__)


@public.route('/api/gamelists')
def public_index():
    return jsonify({
        'gameList': [1, 2, 3, 4, 5]
    })
