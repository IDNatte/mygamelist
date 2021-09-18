from flask import render_template
from flask import Blueprint
from flask import redirect

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect('auth')


@main.route('/auth')
def auth():
    return render_template('auth/index.html.j2')
