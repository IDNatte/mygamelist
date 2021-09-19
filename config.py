# load module to read .env file
from dotenv import dotenv_values

# session config
SECRET_KEY = dotenv_values('.env').get('SECRET_KEY')

# sqlalchemy postgresql config
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432/mgl_db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Auth0 Config
AUTH0_DOMAIN = 'https://informal.us.auth0.com/'
AUTH0_CLIENT = dotenv_values('.env').get('AUTH0_CLIENT_ID')
AUTH0_SECRET = dotenv_values('.env').get('AUTH0_CLIENT_SECRET')
API_AUDIENCE = 'http://127.0.0.1:8000/'
ALGORITHMS = ["RS256"]
