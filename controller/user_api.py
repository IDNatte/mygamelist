from flask import Blueprint
from flask import jsonify

from .controller_helper import ServerError
from .controller_helper import authenticate
from .controller_helper import AuthError
from .controller_helper import authorize

from model import MyGame
from model import Vendor
from model import User
from model import Game

user = Blueprint('user_endpoint', __name__)


@user.route('/api/user/me')
@authenticate
@authorize(permission='get:user-info')
def user_index(user_id):
    user = User.query.get(user_id)
    my_games_id = [game.id for game in user.my_game]
    my_gamelist = MyGame.query.join(Vendor, Game).filter(MyGame.id.in_(my_games_id)).all()
    print(my_gamelist)
    return jsonify({
        'username': user.username,
        'email': user.email,
        'avatar': user.picture,
        'game': {
            'games': [1, 2, 3, 4, 5],
            'totalGame': len(user.my_game)
        }
    })


# Error Handler
@user.errorhandler(AuthError)
@user.errorhandler(ServerError)
def user_errorhandler(error):
    return jsonify({
        'status': error.name,
        'code': error.code,
        'detail': error.description
    }), error.code
