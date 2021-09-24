web: gunicorn --workers=5 --threads=2 "app:init_app()"
worker: . ./script/pre-run.sh && flask db init && flask db migrate && flask db upgrade