from flask import Blueprint
from flask_cors import CORS
from flask import jsonify

from .controller_helper import ServerError
from .controller_helper import AuthError

error = Blueprint('error_endpoint', __name__)

# set cors in blueprint level
CORS(error)


@error.app_errorhandler(403)
@error.app_errorhandler(405)
@error.app_errorhandler(404)
@error.app_errorhandler(422)
@error.app_errorhandler(AuthError)
@error.app_errorhandler(ServerError)
def api_errorhandler(error):
    return jsonify({
        'status': error.name,
        'code': error.code,
        'detail': error.description
    }), error.code
