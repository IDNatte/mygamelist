from flask_migrate import Migrate
from flask_cors import CORS
from flask import Flask

# API endpoint
from controller import public_api
from controller import admin_api
from controller import error_api
from controller import user_api

# common endpoint
from controller import main

# database
from shared import db
# from model import *


def create_app(test_config=None):
    # pylint: disable=assignment-from-no-return

    # initialize apps
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config')

    # initialize extension
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    Migrate().init_app(app=app, db=db)

    # registering blueprint
    app.register_blueprint(public_api.public)
    app.register_blueprint(admin_api.admin)
    app.register_blueprint(error_api.error)
    app.register_blueprint(user_api.user)
    app.register_blueprint(main)

    return app
