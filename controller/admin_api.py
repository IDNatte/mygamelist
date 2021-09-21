from dateutil import parser as dt_ps
from json import JSONDecodeError
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

from .controller_helper import authenticate
from .controller_helper import authorize

from model import Vendor
from model import MyGame
from model import Game
from model import User

admin = Blueprint('admin_endpoint', __name__)
ITEM_LIMIT = 10


# user management endpoint
@admin.route('/api/users')
@authenticate
@authorize(permission='get:user')
@authorize(permission='get:user-game')
def admin_get_user(user_id):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEM_LIMIT
    end = start + ITEM_LIMIT

    users = User.query.all()
    user = [{'user_id': user.id, 'user': user.username, 'email': user.email} for user in users]

    return jsonify({
        'users': user[start:end]
    })


@admin.route('/api/user/<user>')
@authenticate
@authorize(permission='get:user-info')
@authorize(permission='get:user-game')
def admin_user_detail(user_id, user):
    user_detail = User.query.filter(User.id == user).one_or_none()

    if user_detail:
        user_game_id = [game.id for game in user_detail.my_game]
        user_gamelist = MyGame.query.join(Vendor, Game).filter(MyGame.id.in_(user_game_id)).all()

        games = [{
            'list_id': game.id,
            'game_id': game.Game.id,
            'name': game.Game.name,
            'cover': game.Game.cover_link,
            'vendor': {
                'vendor_id': game.Vendor.id,
                'name': game.Vendor.name,
                'distributor': game.Vendor.distributor
            }} for game in user_gamelist]

        return jsonify({
            'username': user_detail.username,
            'email': user_detail.email,
            'avatar': user_detail.picture,
            'game': {
                'games': games,
                'totalGame': len(user_detail.my_game)
            }
        })

    else:
        abort(404, 'No data founded')


# game vendor management endpoint
@admin.route('/api/vendors', methods=['POST'])
@authenticate
@authorize(permission='post:vendor')
def admin_vendor_add(user_id):
    if request.method == 'POST':
        try:
            name = request.get_json()['name']
            distributor = request.get_json()['distributor']
            publisher = request.get_json()['publisher']
            developer = request.get_json()['developer']
            release_date = dt_ps.parse(request.get_json()['release_date'])

            add_vendor = Vendor(name, distributor, publisher, developer, release_date)
            add_vendor.add()

            return jsonify({
                'literal_status': 'saved',
                'content': add_vendor.get()
            }), 201

        except (JSONDecodeError, ValueError, KeyError):
            abort(422, 'Invalid request body')

        except TypeError:
            abort(403, 'Nothing in body')

    else:
        abort(405)


@admin.route('/api/vendor/<int:vendor_id>', methods=['PATCH', 'DELETE'])
@authenticate
@authorize(permission='patch:vendor')
@authorize(permission='delete:vendor')
def admin_vendor_edit_delete(user_id, vendor_id):
    if request.method == 'PATCH':
        vendor = Vendor.query.get(vendor_id)

        if vendor:
            try:

                name = request.get_json()['name']
                distributor = request.get_json()['distributor']
                publisher = request.get_json()['publisher']
                developer = request.get_json()['developer']
                release_date = dt_ps.parse(request.get_json()['release_date'])

                vendor.name = name
                vendor.distributor = distributor
                vendor.publisher = publisher
                vendor.developer = developer
                vendor.release_date = release_date

                vendor.update()

                return jsonify({
                    'literal_status': 'updated',
                    'content': vendor.get()
                })

            except (JSONDecodeError, ValueError, KeyError):
                abort(422, 'Invalid request body')

            except TypeError:
                abort(403, 'Nothing in body')

        else:
            abort(404, 'No data founded')

    elif request.method == 'DELETE':
        vendor = Vendor.query.get(vendor_id)

        if vendor:
            vendor.remove()
            return jsonify({
                'literal_status': 'deleted',
                'list_id': vendor.id
            })

        else:
            abort(404, 'No data founded')
        return jsonify({'test': 'test'})

    else:
        abort(405)


# game list management endpoint
@admin.route('/api/gamelists', methods=['POST'])
@authenticate
@authorize(permission='post:game')
def admin_game_add(user_id):
    if request.method == 'POST':
        try:
            name = request.get_json()['name']
            price = int(request.get_json()['price'])
            rating = int(request.get_json()['price'])
            platform = list(request.get_json()['platform'])
            genre = list(request.get_json()['genre'])
            cover_link = request.get_json()['cover_link']
            vendor = int(request.get_json()['vendor_id'])

            add_game = Game(name, price, rating, platform, genre, cover_link, vendor)
            add_game.add()

            return ({
                'literal_status': 'saved',
                'content': add_game.get()
            })

        except (JSONDecodeError, ValueError, KeyError):
            abort(422, 'Invalid request body')

        except TypeError:
            abort(403, 'Nothing in body')

    else:
        abort(405)


@admin.route('/api/gamelist/<int:game_id>', methods=['PATCH', 'DELETE'])
@authenticate
@authorize(permission='patch:game')
@authorize(permission='delete:game')
def admin_game_edit_delete(user_id, game_id):
    if request.method == 'PATCH':
        game = Game.query.get(game_id)

        if game:
            name = request.get_json()['name']
            price = int(request.get_json()['price'])
            rating = int(request.get_json()['price'])
            platform = list(request.get_json()['platform'])
            genre = list(request.get_json()['genre'])
            cover_link = request.get_json()['cover_link']

            game.name = name
            game.price = price
            game.rating = rating
            game.platform = platform
            game.genre = genre
            game.cover_link = cover_link

            game.update()

            return jsonify({
                'literal_status': 'updated',
                'content': game.get()
            })

        else:
            abort(404, 'No data founded')
        return jsonify({'test': 'test'})

    elif request.method == 'DELETE':
        game = Game.query.get(game_id)

        if game:
            game.remove()
            return jsonify({
                'literal_status': 'deleted',
                'list_id': game.id
            })

        else:
            abort(403, 'Nothing in body')

    else:
        abort(405)
