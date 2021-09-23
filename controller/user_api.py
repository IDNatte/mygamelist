from dateutil import parser as dt_ps
from flask_cors import CORS
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from .controller_helper import authenticate
from .controller_helper import authorize

from model import MyGame
from model import Vendor
from model import User
from model import Game

user = Blueprint('user_endpoint', __name__)
ITEM_LIMIT = 10

# set cors in blueprint level
CORS(user)


@user.route('/api/user/me')
@authenticate
@authorize(permission='get:me')
def user_index(user_id):
    user = User.query.get(user_id)
    my_games_id = [game.id for game in user.my_game]
    my_gamelist = MyGame.query.join(Vendor, Game).filter(MyGame.id.in_(my_games_id)).all()

    games = [{
        'list_id': game.id,
        'game_id': game.Game.id,
        'name': game.Game.name,
        'cover': game.Game.cover_link,
        'vendor': {
            'vendor_id': game.Vendor.id,
            'name': game.Vendor.name,
            'distributor': game.Vendor.distributor
        }} for game in my_gamelist]

    return jsonify({
        'username': user.username,
        'email': user.email,
        'avatar': user.picture,
        'game': {
            'games': games,
            'totalGame': len(user.my_game)
        }
    })


@user.route('/api/user/me/games', methods=['GET', 'POST'])
@authenticate
@authorize(permission='get:my-game')
@authorize(permission='post:my-game')
def user_gamelist(user_id):
    if request.method == 'GET':
        games = MyGame.query.join(Vendor, Game).filter(MyGame.owner == user_id).all()
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * ITEM_LIMIT
        end = start + ITEM_LIMIT

        my_game_lists = [{
            'list_id': game.id,
            'game_id': game.Game.id,
            'name': game.Game.name,
            'platform': game.Game.platform,
            'genres': game.Game.genre,
            'cover': game.Game.cover_link,
            'vendor': {
                'vendor_id': game.Vendor.id,
                'name': game.Vendor.name,
                'distributor': game.Vendor.distributor
            }
        } for game in games]

        return jsonify({
            'myGames': my_game_lists[start:end],
            'totalGames': len(my_game_lists)
        })

    elif request.method == 'POST':
        try:
            owner = user_id
            purchased = dt_ps.parse(request.get_json()['purchased_on'])
            game = int(request.get_json()['game_id'])
            vendor = int(request.get_json()['vendor_id'])

            add_my_game = MyGame(owner=owner, purchased_on=purchased, game=game, vendor=vendor)
            add_my_game.add()

            return jsonify({
                'literal_status': 'saved',
                'list_id': add_my_game.id
            }), 201

        except (ValueError, KeyError):
            abort(422, 'Invalid request body')

        except TypeError:
            abort(403, 'Nothing in body')

    else:
        abort(405)


@user.route('/api/user/me/games/<int:my_game_id>', methods=['PATCH', 'DELETE'])
@authenticate
@authorize(permission='patch:my-game')
@authorize(permission='delete:my-game')
def user_edit_delete_gamelist(user_id, my_game_id):
    if request.method == 'PATCH':
        try:
            play_status = request.get_json()['play_status']
            game = MyGame.query.get(my_game_id)

            if game:

                game.play_status = play_status
                game.update()

                return jsonify({
                    'literal_status': 'updated',
                    'content': game.get()
                })

            else:
                abort(404, 'No data founded')

        except (ValueError, KeyError):
            abort(422, 'Invalid request body')

        except TypeError:
            abort(403, 'Nothing in body')

    elif request.method == 'DELETE':
        game = MyGame.query.get(my_game_id)
        if game:
            game.remove()
            return jsonify({
                'literal_status': 'deleted',
                'list_id': game.id
            })

        else:
            abort(404, 'No data founded')

    else:
        abort(405)
