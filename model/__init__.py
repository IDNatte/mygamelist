from shared import db


class Vendor(db.Model):
    # pylint: disable=maybe-no-member
    __tablename__ = 'Vendor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    distributor = db.Column(db.String(150), nullable=False)
    publisher = db.Column(db.String(150), nullable=False)
    developer = db.Column(db.String(150), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)

    # relationship
    my_game = db.relationship('MyGame', backref='Vendor', lazy=True, cascade='all, delete-orphan')
    game_lists = db.relationship('Game', backref='Vendor', lazy=True, cascade='all, delete-orphan')


class Game(db.Model):
    # pylint: disable=maybe-no-member
    __tablename__ = 'Game'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.ARRAY(db.String), nullable=False)
    genre = db.Column(db.ARRAY(db.String), nullable=True)
    cover_link = db.Column(db.String(200), nullable=True)
    vendor = db.Column(db.Integer, db.ForeignKey('Vendor.id'), nullable=False)

    # relationship
    my_game = db.relationship('MyGame', backref='Game', lazy=True, cascade='all, delete-orphan')


class MyGame(db.Model):
    # pylint: disable=maybe-no-member
    __tablename__ = 'Mygame'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String, db.ForeignKey('Auth0user.id'), nullable=False)
    play_status = db.Column(db.Boolean, default=False)
    purchased_on = db.Column(db.DateTime, nullable=False)
    game = db.Column(db.Integer, db.ForeignKey('Game.id'), nullable=False)
    vendor = db.Column(db.Integer, db.ForeignKey('Vendor.id'), nullable=False)


class User(db.Model):
    # pylint: disable=maybe-no-member
    __tablename__ = 'Auth0user'

    id = db.Column(db.String, primary_key=True, nullable=False)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    picture = db.Column(db.String(255), nullable=False, unique=True)

    # relationship
    my_game = db.relationship('MyGame', backref='User', lazy=True, cascade='all, delete-orphan')
