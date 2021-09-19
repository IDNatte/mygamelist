"""
Controller helper
"""
from flask import current_app
from functools import wraps
from flask import request
from jose import jwt
import requests

# debug
# import pprint


class AuthError(Exception):
    """
    Authentication error

    Error related to Authentication.
    """
    def __init__(self, name, description, code):
        self.name = name
        self.code = code
        self.description = description


class ServerError(Exception):
    """
    Server fault error

    Raised during undetermined exception.
    """
    def __init__(self, name, description, detail, code):
        self.name = name
        self.code = code
        self.detail = detail
        self.description = description


def Auth0Validator(token):
    """
    Auth0Validator

    non-decorator Auth0 token validator function
    """

    try:
        url = current_app.config.get('AUTH0_DOMAIN')
        wks_url = f'{url}.well-known/jwks.json'
        wks_key = requests.get(wks_url)

        unverif_token = jwt.get_unverified_header(token)

        rsa_key = {}
        for k in wks_key.json().get('keys'):
            if k.get('kid') == unverif_token.get('kid'):
                rsa_key.update({
                    "kty": k.get("kty"),
                    "kid": k.get("kid"),
                    "use": k.get("use"),
                    "n": k.get("n"),
                    "e": k.get("e")
                })

        if rsa_key:
            try:
                payload = jwt.decode(token,
                                     rsa_key,
                                     algorithms=current_app.config.get('ALGORITHMS'),
                                     audience=current_app.config.get('API_AUDIENCE'),
                                     issuer=url)

                return payload

            except jwt.ExpiredSignatureError:
                raise AuthError('Expired Token', 'token expiration reached', 401)

            except jwt.JWTClaimsError:
                raise AuthError('Unauthoriozed', 'Unrecognized issuer', 401)

            except Exception as e:
                raise ServerError('Server Fault', 'Unrecognized server fault', e, 500)

        else:
            raise AuthError('Unauthoriozed', 'Invalid token entity', 401)

    except jwt.JWTError:
        raise AuthError('Unauthoriozed', 'Broken jwt payload', 401)


def Auth0Identifier(user):
    """
    Auth0 user identificator

    non-decorator Auth0 user identificator function
    """

    client = current_app.config.get('AUTH0_CLIENT')
    secret = current_app.config.get('AUTH0_SECRET')
    aud = 'https://informal.us.auth0.com/api/v2/'
    url = current_app.config.get('AUTH0_DOMAIN')
    gt = 'client_credentials'

    payload = {
        "client_id": client,
        "client_secret": secret,
        "audience": aud,
        "grant_type": gt
    }

    authorize = requests.post(f'{url}oauth/token', data=payload)

    if authorize.status_code == 200:
        token = authorize.json().get('access_token')
        token_type = authorize.json().get('token_type')

        server_headers = {
            "authorization": f'{token_type} {token}'
        }

        user = requests.get(f'{url}api/v2/users/{user}', headers=server_headers)

        user_payload = {
            "user_id": user.json().get('identities')[0].get('user_id'),
            "username": user.json().get('nickname'),
            "email": user.json().get('email'),
            "picture": user.json().get('picture')
        }

        return user_payload
    else:
        authorize.status_code
        raise ServerError('Server Fault',
                          'Unrecognized server fault',
                          f'Server transaction error {authorize.status_code}',
                          500)


def auth_header_parser(headers):
    """
    Authorization header parser
    """
    parser = headers.split(' ')

    if len(parser) == 2:
        if 'Bearer' in parser:
            return parser[1]
        else:
            raise AuthError('Unauthoriozed', 'Broken Authorization header', 401)
    else:
        raise AuthError('Unauthoriozed', 'Missing token', 401)


def rbac_checker(payload, permission):
    if payload.get('permissions'):
        if permission in payload.get('permissions'):
            return True
        else:
            return False
    else:
        raise AuthError('Unauthoriozed', 'Permissions unauthorized', 401)


def authenticate(f):
    """
    endpoint authentication decorator
    """
    @wraps(f)
    def authenticate_decorator(*args, **kwargs):
        try:
            headers = request.headers['Authorization']
            token = auth_header_parser(headers)
            validator = Auth0Validator(token)
            if validator:
                user_obj = validator.get('sub')
                user_id = Auth0Identifier(user_obj).get('user_id')
                return f(user_id, *args, **kwargs)
            else:
                return False
        except KeyError:
            raise AuthError('Unauthoriozed', 'Broken Authorization header', 401)

    return authenticate_decorator


def authorize(permission=''):
    def authorization_decorator(f):
        @wraps(f)
        def wrapper_func(*args, **kwargs):
            try:
                headers = request.headers['Authorization']
                token = auth_header_parser(headers)
                payload = Auth0Validator(token)
                check_permission = rbac_checker(payload, permission)
                if check_permission:
                    return f(*args, **kwargs)
                else:
                    raise AuthError('Unauthoriozed', 'Permissions unauthorized', 401)

            except KeyError:
                raise AuthError('Unauthoriozed', 'Broken Authorization header', 401)

        return wrapper_func
    return authorization_decorator
