# My Gamelist

Explore your game

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


## Flask 2.0 Bug

- `TypeError: exceptions must derive from BaseException` [**referenced in here**](https://stackoverflow.com/a/68712238) for time being use `--eager-loading` flag instead to avoid raising this error in development mode, fixed in `flask 2.0.2` release.