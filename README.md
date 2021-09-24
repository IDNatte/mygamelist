# My Gamelist

Explore your game

## Requirements

Below is minimal requirements for running server locally.

- Python 3.8 or latest
- Postgresql 13
- [Auth0](https://auth0.com) Account

## Before Run

Before running server locally, you should prepare local database, Auth0 account with bellow config, copying .env.example to .env, and installing requirement in requirements.txt.

### Project structure
bellow is project structure

```
- final-project
    |
    | - env (python virtual environment)
    |
    | - controller module (controller/router/Blueprint)
    |   |
    |   | - controller_helper module (controller helper such as decorator, auth0authenticator, etc.)
    |   |
    |   | - __init__.py (authenticatin, and login blueprint)
    |   |
    |   | - admin_api.py (admin endpoint blueprint)
    |   |
    |   | - error_api.py (error endpoint blueprint)
    |   |
    |   | - public_api.py (public endpoint blueprint)
    |   |
    |   | - user_api.py (user endpoint blueprint)
    |   |---------------------------------------------------------->
    |
    | - migrations (database migration module)
    |
    | - model
    |   |
    |   | - model_helper module (model helper such as random id generator, Etc.)
    |   |
    |   | - __init__.py (model modules)
    |   |---------------------------------------------------------->
    |
    | - script
    |   |
    |   | - pre-run.sh (script for defining environment variable before running flask command)
    |   |---------------------------------------------------------->
    |
    | - static (static files folder)
    |
    | - templates (templates folder)
    |
    | - .env.examples (.env example file)
    |
    | - app.py (main entripoint application)
    |
    | - config.py (main entripoint configuration files)
    |
    | - Procfile (heroku config file)
    |
    | - README.md (documentation file)
    |
    | - requirements.txt (python dependencies lists)
    |
    | - shared.py (shared python variables, used for defining shared variable such as db = SQLAlchemy())
    |
    | - test_app.py (test file runner)
    |
    |---------------------------------------------------------->

```

### Python Virtual Environment

for running locally, it is recommended to use python 3.8 environment

to set up python 3.8 env in terminal, you can type
```
user@computer /backend $ python -m venv env
```

### Auth0 Config
before running server, make sure you have been register Auth0 account, and then for the Auth0 config you can follow step bellow

- Create new Application named `My Gamelist` and in setting.
    - Set application type for `Single Page`.
    - Set allowed callback to http://127.0.0.1:8000/auth.
    - Then save changes.
- Create new API for Auth0 application.
    - Set name as `My Gamelist API`
    - Set Identifier as `http://127.0.0.1:8000/` this step is crucial, do not make mistake if you setting this otherwise you should make a new API again.
    - after creating API in setting set `Enable RBAC` and `Add permission to Access Token` to true.
- After creating new api, you need to define some permission in permission tab
    - `delete:my-game`
    - `get:me`
    - `get:my-game`
    - `patch:my-game`
    - `post:my-game`
    - `delete:game`
    - `delete:vendor`
    - `get:user`
    - `get:user-game`
    - `get:user-info`
    - `patch:game`
    - `patch:vendor`
    - `post:game`
    - `post:vendor`

- After adding new permission, create 2 new role with and assign permission.
    - roles `mgl_user` with permission
        - `get:me`
        - `get:my-game`
        - `post:my-game`
        - `patch:my-game`
        - `delete:my-game`

    - roles `mgl_manager` with permission
        - `get:user`
        - `get:user-info`
        - `get:user-game`
        - `post:game`
        - `post:vendor`
        - `patch:game`
        - `patch:vendor`
        - `delete:game`
        - `delete:vendor`



### .env config file
after creating and configuring Auth0, then don't forget to copy paste the .env.example file to .env.
.env file required for set some environment variables that needed such as Auth0 Client id, app client id, Etc.

after done copying and renaming .env.example, bellow is what you need to change inside .env files
- `SECRET_KEY` set this value to a random string, you can use string randomizer from google.
- `AUTH0_DOMAIN` set this value to define Auth0 domain, you can find it in application setting under Domain.
- `AUTH0_CLIENT_ID` this is your management client id, **It is different** from `My Gamelist` Client_id taht you configure earlier this id needed to get your user account information, you can get it by following [this documentation](https://auth0.com/docs/security/tokens/access-tokens/get-management-api-access-tokens-for-production) step.
- `AUTH0_CLIENT_SECRET` this is your management client secret, **It is different** from `My Gamelist` Client_secret that you configure earlier this id needed to get your user account information, you can get it by following [this documentation](https://auth0.com/docs/security/tokens/access-tokens/get-management-api-access-tokens-for-production) step.
- `AUTH0_APP_CLIENT_ID` this value is needed for generating Auth0 url in `/login`, so that you can test your application.
- `AUTH0_API_AUDIENCE` this value is your identifier for `My Gamelist API` that you set earlier.
- `AUTH0_SYSTEM_AUDIENCE` this is your management endpoint E.g `https://mydomain.us.auth0.com/api/v2/` you can found it in [here](https://auth0.com/docs/support/policies/public-cloud-service-endpoints)
- `AUTH0_AUTH_ALGORITHMS` this is your Auth0 hash algorithms usually it is `["RS256"]` by default.
- `AUTH0_SYSTEM_GRANT_TYPE` this is your management grant type, by default you want to set this to `client_credentials`
- `USER_TEST` this value used for running `test_application.py`, this value is your user token with role `mgl_user`.
- `MANAGER_TEST` this value used for running `test_application.py`, this value is your user token with role `mgl_manager`.

### Database

for database configuration, you can modify value `SQLALCHEMY_DATABASE_URI` in file config.py.
make sure you has been creating new database caled `mgl_db` if you not modifying `SQLALCHEMY_DATABASE_URI` parameter in config.py
for migrating database you can type 
```
(env) user@computer /backend $ . ./script/pre-run.sh
(env) user@computer /backend $ flask db migrate
(env) user@computer /backend $ flask db upgrade
```

## Run server

To run server you can either define env_var from bash directly, or use pre-run script that already defined.
(only work for MacOS or Linux OS)

This server is run on port 8000 by default if you using bash script to set flask env_var, and will run in port 5000 if you set it manualy, or you can set flag `--port <PORT>` when running flask run.


- directly define FLASK_ENV and FLASK_APP

```
(env) user@computer /backend $ export FLASK_APP=app && export FLASK_ENV=development
*! (env) user@computer /backend $ flask run --port <PORT> --eager-loading
```

- using pre-run script
```
(env) user@computer /backend $ . ./script/pre-run.sh
*! (env) user@computer /backend $ flask run --eager-loading
```

**Notice**

***! (Read Flask 2.0 Bug)**


## Endpoint
for accessing endpoint you can go to `/login` page
there you will be provided with an Auth0 login link, you can copy and paste that link and get your user access token

the `/auth` page will testing automatically registering your account to local database,
if you accesing this via `SPA Application` you can send a post request to `/auth/token` otherwise you will be unable to accesing endpoint even you get a valid Auth0 jwt token.

```
Server : http://127.0.0.1:8000/ or http://localhost:8000/

Login page : /login
Token Cheker : /auth/token
API Endpoint : /api/<endpoint>
```

### Public Endpoint
this endpoint don't need access token in header

#### Get game lists
```
Endpoint : /api/gamelists
Method : "GET"
Header : not required
body : not required
related error: 405

request : GET http://localhost:8000/api/gamelists or GET http://localhost:8000/api/gamelists?page=1

response : <200> Object {
    "games": array,
    "totalGames": integer (length of requested gamelists in a page if provided in url parameter, default 10)
}
```

#### Get game detail
```
Endpoint : /api/gamelists
Method : "GET"
Header : not required
body : not required
related error: 404, 405

request : GET http://localhost:8000/api/gamelist/<game_id>

response : <200> Array {
    "gameName": string,
    "rating": integer,
    "price": integer,
    "genre": string array,
    "platform": string array,
    "cover": url string,
    "releaseDate": datetime string,
    "vendor": object {
        "name": string,
        "publisher": string,
        "distributor": string,
        "developer": string
    }
}
```

#### Get vendor lists
```
Endpoint : /api/vendors
Method : "GET"
Header : not required
body : not required
related error: 405

request : GET http://localhost:8000/api/vendors or GET http://localhost:8000/api/vendors?page=1

response : <200> Object {
    "vendors": array,
    "total": integer (length of requested vendor lists in a page if provided in url parameter, default 10)
}
```

#### Get vendor detail
```
Endpoint : /api/gamelists
Method : "GET"
Header : not required
body : not required
related error: 404, 405

request : GET http://localhost:8000/api/vendor/<vendor_id>

response : <200> Object {
    "name": string,
    "publisher": string,
    "distributor": string,
    "developer": string,
    "games": array
}
```

### User Endpoint
this endpoint is required authentication header

#### Get user info
```
Endpoint : /api/user/me
Method : "GET"
Header : authorization type Bearer
body : not required
related error: 405, 401

request : GET http://localhost:8000/api/user/me

response : <200> Object {
    "avatar": url string,
    "email": email string,
    "game": object {
        "games": array,
        "totalGame": integer
    },
    "username": string
}
```

#### Get my gamelist
```
Endpoint : /api/user/me/games
Method : "GET"
Header : authorization type Bearer
body : not required
related error: 405, 401

request : GET http://localhost:8000/api/user/me/games

response : <200> Object {
    "myGames": array,
    "totalGames": integer (length of requested gamelists in a page if provided in url parameter, default 10)
}
```

#### Crete my gamelist
```
Endpoint : /api/user/me/games
Method : "POST"
Header : authorization type Bearer
body : required
related error: 405, 401, 403, 422

request : POST http://localhost:8000/api/user/me/games
request body : {
    "vendor_id": <vendor_id (integer)>,
    "game_id": <game_id (integer)>,
    "purchased_on": datetime string
}

response : <201> Object {
    "literal_status": string (informational success status by server),
    "list_id": integer
}
```

#### Editing play status
```
Endpoint : /api/user/me/games/<list_id>
Method : "PATCH"
Header : authorization type Bearer
body : required
related error: 401, 403, 404, 422

request : PATCH http://localhost:8000/api/user/me/games/6
request body : {
    "play_status": Boolean,
}

response : <200> Object {
    "literal_status": string (informational success status by server),
    "content": Object
}
```

#### Deleting game from gamelist
```
Endpoint : /api/user/me/games/<list_id>
Method : "DELETE"
Header : authorization type Bearer
body : not required
related error: 404, 405

request : DELETE http://localhost:8000/api/user/me/games/6

response : <200> Object {
    "literal_status": string (informational success status by server),
    "list_id": integer (deleted content id)
}
```

### Admin Endpoint
this endpoint is required authentication header

#### Add new game
```
Endpoint : /api/gamelists
Method : "POST"
Header : authorization type Bearer
body : required
related error: 405, 401, 403, 422

request : POST http://localhost:8000/api/gamelists
request body : {
    "name": string,
    "price": integer,
    "rating": integer,
    "platform": array,
    "genre": array,
    "cover_link": url string,
    "vendor_id": <vendor_id (integer)>
}

response : <201> Object {
    "literal_status": string (informational success status by server),
    "game_id": integer
}
```

#### Edit game
```
Endpoint : /api/gamelist/<game_id>
Method : "PATCH"
Header : authorization type Bearer
body : required
related error: 401, 403, 404, 405, 422

request : PATCH http://localhost:8000/api/gamelist/6
request body : {
    "name": string,
    "price": integer,
    "rating": integer,
    "platform": array,
    "genre": array,
    "cover_link": url string
}

response : <200> Object {
    "literal_status": string (informational success status by server),
    "content": object
}
```

#### Delete game
```
Endpoint : /api/gamelist/<game_id>
Method : "DELETE"
Header : authorization type Bearer
body : not required
related error: 404, 405

request : DELETE http://localhost:8000/api/gamelist/6

response : <200> Object {
    "literal_status": string (informational success status by server),
    "game_id": integer
}
```

#### Add new vendor
```
Endpoint : /api/vendors
Method : "POST"
Header : authorization type Bearer
body : required
related error: 405, 401, 403, 422

request : POST http://localhost:8000/api/vendors
request body : {
    "name": string,
    "developer": string,
    "distributor": string,
    "publisher": string,
    "release_date": datetime string
}

response : <201> Object {
    "literal_status": string (informational success status by server),
    "content": object
}
```

#### Edit vendor
```
Endpoint : /api/vendor/<vendor_id>
Method : "PATCH"
Header : authorization type Bearer
body : required
related error: 401, 403, 404, 405, 422

request : PATCH http://localhost:8000/api/gamelist/6
request body : {
    "name": string,
    "price": integer,
    "rating": integer,
    "platform": array,
    "genre": array,
    "cover_link": url string
}

response : <200> Object {
    "literal_status": string (informational success status by server),
    "content": object
}
```

#### Delete vendor
```
Endpoint : /api/gamelist/<game_id>
Method : "DELETE"
Header : authorization type Bearer
body : not required
related error: 404, 405

request : DELETE http://localhost:8000/api/gamelist/6

response : <200> Object {
    "literal_status": string (informational success status by server),
    "vendor_id": integer
}
```

#### User list
```
Endpoint : /api/users
Method : "GET"
Header : authorization type Bearer
body : not required
related error: 405

request : GET http://localhost:8000/api/users or GET http://localhost:8000/api/users?page=1

response : <200> Object {
    "users": arrays
}
```

#### Get user detail 
```
Endpoint : /api/user/<user_id>
Method : "GET"
Header : authorization type Bearer
body : not required
related error: 404, 405

request : GET http://localhost:8000/api/user/61470d6d44672c00694cfd14

response : <200> Object {
    "avatar": url string,
    "email": email string,
    "game": object {
        "games": array,
        "totalGame": integer
    },
    "username": string
}
```

## Known Issue

- `TypeError: exceptions must derive from BaseException` [**referenced in here**](https://stackoverflow.com/a/68712238) for time being use `--eager-loading` flag instead to avoid raising this error in development mode, fixed in `flask 2.0.2` release.

- `Database heroku` https://stackoverflow.com/a/64698899