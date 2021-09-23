from flask import render_template
from flask_cors import CORS
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import request
from flask import jsonify
from flask import abort

from .controller_helper import Auth0Identifier
from .controller_helper import Auth0Validator

from model import User
from shared import db

main = Blueprint('main', __name__)

# set cors in blueprint level
CORS(main)


@main.route('/')
def index():
    return redirect('auth')


@main.route('/auth')
def auth():
    return render_template('auth/index.html.j2')


@main.route('/auth/token', methods=['POST'])
def get_token():
    # pylint: disable=maybe-no-member
    if request.method == 'POST':
        try:
            token = request.get_json()['token']
            auth0_validator = Auth0Validator(token).get('sub')
            auth0_user_object = Auth0Identifier(auth0_validator)
            auth0_user_id = auth0_user_object.get('user_id')

            local_user = User.query.filter(User.id == auth0_user_id).one_or_none()

            if local_user:
                return jsonify({
                    'user_status': 'fetched',
                    'literal_status': 'redirect',
                    'redirect': url_for('user_endpoint.user_index')
                })

            else:
                user_id = auth0_user_id
                username = auth0_user_object.get('username')
                email = auth0_user_object.get('email')
                picture = auth0_user_object.get('picture')
                role = auth0_user_object.get('role')

                user = User(id=user_id, username=username, email=email, picture=picture, role=role)
                db.session.add(user)
                db.session.commit()

                return jsonify({
                    'user_status': 'create',
                    'literal_status': 'redirect',
                    'redirect': url_for('user_endpoint.user_index')
                })

        except KeyError:
            abort(422)
    else:
        abort(405)
