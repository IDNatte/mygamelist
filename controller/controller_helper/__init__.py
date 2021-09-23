"""
Controller helper
"""
from flask import current_app
from functools import wraps
from flask import request
from jose import jwt
import requests
import datetime

from model import SystemAuthKey
from shared import db


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
                                     algorithms=current_app.config.get('AUTH0_ALGORITHMS'),
                                     audience=current_app.config.get('AUTH0_API_AUDIENCE'),
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
    # pylint: disable=maybe-no-member

    current_time = datetime.datetime.now()
    url = current_app.config.get('AUTH0_DOMAIN')

    token_query = SystemAuthKey.query
    expired_token = token_query.filter(SystemAuthKey.expiration <= current_time)
    token = token_query.order_by(SystemAuthKey.expiration.desc())\
        .filter(SystemAuthKey.expiration >= current_time)\
        .first()

    if token:
        counter = token_query.order_by(SystemAuthKey.expiration.desc()).count()
        user_data = requests.get(f'{url}api/v2/users/{user}', headers={
            "authorization": f'Bearer {token.token}'
        })

        roles = requests.get(f'{url}api/v2/users/{user}/roles', headers={
            "authorization": f'Bearer {token.token}'
        })

        if counter > 1:
            expired_token.delete()
            db.session.commit()

        return {
            "user_id": user_data.json().get('identities')[0].get('user_id'),
            "username": user_data.json().get('nickname'),
            "email": user_data.json().get('email'),
            "picture": user_data.json().get('picture'),
            "role": roles.json()[0].get('name')
        }

    else:
        authorize = requests.post(f'{url}oauth/token', data={
            "client_id": current_app.config.get('AUTH0_CLIENT'),
            "client_secret": current_app.config.get('AUTH0_SECRET'),
            "audience": current_app.config.get('AUTH0_SYSTEM_AUDIENCE'),
            "grant_type": current_app.config.get('AUTH0_GRANT_TYPE')
        })

        if authorize.status_code == 200:
            token = authorize.json().get('access_token')
            token_type = authorize.json().get('token_type')

            token_time = datetime.timedelta(seconds=authorize.json().get('expires_in'))
            current_time = datetime.datetime.now()
            token_expire_time = current_time + token_time

            securityToken = SystemAuthKey(token=token, expiration=token_expire_time)
            securityToken.save()

            user = requests.get(f'{url}api/v2/users/{user}', headers={
                "authorization": f'{token_type} {securityToken.token}'
            })

            return {
                "user_id": user.json().get('identities')[0].get('user_id'),
                "username": user.json().get('nickname'),
                "email": user.json().get('email'),
                "picture": user.json().get('picture')
            }

        else:
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
            raise AuthError('Unauthorized', 'Broken Authorization header', 401)

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
