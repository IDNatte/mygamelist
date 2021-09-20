# load module to read .env file
from dotenv import dotenv_values

# session config
SECRET_KEY = dotenv_values('.env').get('SECRET_KEY')

# sqlalchemy postgresql config
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/mgl_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Auth0 Config
AUTH0_DOMAIN = dotenv_values('.env').get('AUTH0_AUTHENTICATION_URL')
AUTH0_CLIENT = dotenv_values('.env').get('AUTH0_CLIENT_ID')
AUTH0_SECRET = dotenv_values('.env').get('AUTH0_CLIENT_SECRET')

AUTH0_SYSTEM_AUDIENCE = dotenv_values('.env').get('AUTH0_SYSTEM_AUDIENCE')
AUTH0_API_AUDIENCE = dotenv_values('.env').get('AUTH0_API_AUDIENCE')

AUTH0_ALGORITHMS = dotenv_values('.env').get('AUTH0_AUTH_ALGORITHMS')
AUTH0_GRANT_TYPE = dotenv_values('.env').get('AUTH0_SYSTEM_GRANT_TYPE')
