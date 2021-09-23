from flask_cors import CORS
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import abort

from model import Vendor
from model import Game
from shared import db

public = Blueprint('public_endpoint', __name__)
ITEM_LIMIT = 10

# set cors in blueprint level
CORS(public)


@public.route('/api/gamelists')
def public_games():
    # pylint: disable=maybe-no-member

    game_lists = []
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEM_LIMIT
    end = start + ITEM_LIMIT

    games = db.session.query(Game, Vendor).join(Vendor).filter(Vendor.id == Game.vendor).all()

    for x in games:
        game_lists.append({
            'game_id': x[0].id,
            'gameName': x[0].name,
            'rating': x[0].rating,
            'price': x[0].price,
            'cover': x[0].cover_link,
            'vendor': {
                'name': x[1].name,
                'distributor': x[1].distributor,
            }
        })

    return jsonify({
        'games': game_lists[start:end],
        'total': len(game_lists)
    })


@public.route('/api/gamelist/<int:game_id>')
def public_game_detail(game_id):
    # pylint: disable=maybe-no-member

    game = db.session.query(Game, Vendor)\
        .join(Vendor)\
        .filter(Game.id == game_id, Vendor.id == Game.vendor)\
        .one_or_none()

    if game:
        return jsonify({
            'gameName': game[0].name,
            'rating': game[0].rating,
            'price': game[0].price,
            'genre': game[0].genre,
            'platform': game[0].platform,
            'cover': game[0].cover_link,
            'releaseDate': game[1].release_date,
            'vendor': {
                'name': game[1].name,
                'publisher': game[1].publisher,
                'distributor': game[1].distributor,
                'developer': game[1].developer,
            }
        })
    else:
        abort(404, 'No data founded')


@public.route('/api/vendors')
def public_vendors():

    vendor_lists = []
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * ITEM_LIMIT
    end = start + ITEM_LIMIT

    vendors = Vendor.query.all()

    for vendor in vendors:
        vendor_lists.append({
            'name': vendor.name,
            'vendor_id': vendor.id
        })

    return jsonify({
        'vendors': vendor_lists[start:end],
        'total': len(vendor_lists)
    })


@public.route('/api/vendor/<int:vendor_id>')
def public_vendor_detail(vendor_id):
    vendor = Vendor.query.filter(Vendor.id == vendor_id).one_or_none()

    if vendor:
        return jsonify({
            'name': vendor.name,
            'publisher': vendor.publisher,
            'distributor': vendor.distributor,
            'developer': vendor.developer,
            'games': [{'game': game.name, 'id': game.id, 'cover': game.cover_link} for game in vendor.game_lists]
        })

    else:
        abort(404, 'No data founded')
