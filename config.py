# load module to read .env file
from dotenv import dotenv_values
import os


# sqlalchemy postgresql config

SQLALCHEMY_TRACK_MODIFICATIONS = False

# secret key switcher

if os.environ.get('FLASK_ENV') == 'development':
    # if environment is development then use .env files

    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/mgl_db'
    # session config
    SECRET_KEY = dotenv_values('.env').get('SECRET_KEY')

    # Auth0 Config
    AUTH0_DOMAIN = dotenv_values('.env').get('AUTH0_DOMAIN')
    AUTH0_CLIENT = dotenv_values('.env').get('AUTH0_CLIENT_ID')
    AUTH0_APP_CLIENT = dotenv_values('.env').get('AUTH0_APP_CLIENT')
    AUTH0_SECRET = dotenv_values('.env').get('AUTH0_CLIENT_SECRET')

    AUTH0_SYSTEM_AUDIENCE = dotenv_values('.env').get('AUTH0_SYSTEM_AUDIENCE')
    AUTH0_API_AUDIENCE = dotenv_values('.env').get('AUTH0_API_AUDIENCE')

    AUTH0_ALGORITHMS = dotenv_values('.env').get('AUTH0_AUTH_ALGORITHMS')
    AUTH0_GRANT_TYPE = dotenv_values('.env').get('AUTH0_SYSTEM_GRANT_TYPE')

else:
    # else if use environment variables instead.

    # use for deploying @ heroku
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB')
    # session config
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Auth0 Config
    AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
    AUTH0_CLIENT = os.environ.get('AUTH0_CLIENT_ID')
    AUTH0_APP_CLIENT = os.environ.get('AUTH0_APP_CLIENT')
    AUTH0_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')

    AUTH0_SYSTEM_AUDIENCE = os.environ.get('AUTH0_SYSTEM_AUDIENCE')
    AUTH0_API_AUDIENCE = os.environ.get('AUTH0_API_AUDIENCE')

    AUTH0_ALGORITHMS = os.environ.get('AUTH0_AUTH_ALGORITHMS')
    AUTH0_GRANT_TYPE = os.environ.get('AUTH0_SYSTEM_GRANT_TYPE')
