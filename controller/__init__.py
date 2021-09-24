from flask import render_template
from flask import current_app
from flask_cors import CORS
from flask import Blueprint
from flask import url_for
from flask import request
from flask import jsonify
from flask import abort

from pygments.formatters import HtmlFormatter
from markdown.extensions import fenced_code
from markdown.extensions import codehilite
from markdown import markdown

from .controller_helper import Auth0Identifier
from .controller_helper import Auth0Validator

from model import User
from shared import db

main = Blueprint('main', __name__)

# set cors in blueprint level
CORS(main)


@main.route('/')
def index():
    with open('README.md') as md:
        docs = markdown(md.read(), extensions=["fenced_code", "codehilite"])

    formatter = HtmlFormatter(style='colorful', full=True, cssclass="codehilite")
    css_string = formatter.get_style_defs()
    md_css_string = f'<style>{css_string}</style>'
    md_template = f'{md_css_string}{docs}'
    return md_template


@main.route('/login')
def login_link():
    domain = current_app.config.get('AUTH0_DOMAIN')
    cid = current_app.config.get('AUTH0_APP_CLIENT')
    audience_redir = current_app.config.get('AUTH0_API_AUDIENCE')

    login_link = f'{domain}authorize?response_type=token&client_id={cid}&redirect_uri={audience_redir}auth&audience={audience_redir}'

    return render_template('login/index.html.j2', login_url=login_link)


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
                    'redirect': url_for('user_endpoint.user_index'),
                    'user_level': local_user.role
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
                    'redirect': url_for('user_endpoint.user_index'),
                    'user_level': local_user.role
                })

        except KeyError:
            abort(422)
    else:
        abort(405)
