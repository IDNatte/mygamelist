from .model_helper import random_id_generator
from shared import db


class Vendor(db.Model):
    # pylint: disable=maybe-no-member
    __tablename__ = 'Vendor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    distributor = db.Column(db.String(150), nullable=False)
    publisher = db.Column(db.String(150), nullable=False, unique=True)
    developer = db.Column(db.String(150), nullable=False, unique=True)
    release_date = db.Column(db.DateTime, nullable=False)

    # relationship
    my_game = db.relationship('MyGame', backref='Vendor', lazy=True, cascade='all, delete-orphan')
    game_lists = db.relationship('Game', backref='Vendor', lazy=True, cascade='all, delete-orphan')

    # serializers
    def __init__(self, name, distributor, publisher, developer, release_date):
        self.name = name
        self.distributor = distributor
        self.publisher = publisher
        self.developer = developer
        self.release_date = release_date

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def get(self):
        return {
            'vendor_id': self.id,
            'vendor_name': self.name,
            'distributor': self.distributor,
            'publisher': self.publisher,
            'developer': self.developer,
            'release_date': self.release_date
        }


class Game(db.Model):
    # pylint: disable=maybe-no-member
    __tablename__ = 'Game'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    platform = db.Column(db.ARRAY(db.String), nullable=False)
    genre = db.Column(db.ARRAY(db.String), nullable=True)
    cover_link = db.Column(db.String(200), nullable=True)
    vendor = db.Column(db.Integer, db.ForeignKey('Vendor.id'), nullable=False)

    # relationship
    my_game = db.relationship('MyGame', backref='Game', lazy=True, cascade='all, delete-orphan')

    # serializer
    def __init__(self, name, price, rating, platform, genre, cover_link, vendor):
        self.name = name
        self.price = price
        self.rating = rating
        self.platform = platform
        self.genre = genre
        self.cover_link = cover_link
        self.vendor = vendor

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def get(self):
        return {
            'game_id': self.id,
            'game_name': self.name,
            'price': self.price,
            'rating': self.rating,
            'platform': self.platform,
            'genre': self.genre,
            'cover': self.cover_link,
            'vendor_id': self.vendor
        }


class MyGame(db.Model):
    # pylint: disable=maybe-no-member
    __tablename__ = 'Mygame'

    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String, db.ForeignKey('Auth0user.id'), nullable=False)
    play_status = db.Column(db.Boolean, default=False)
    purchased_on = db.Column(db.DateTime, nullable=False)
    game = db.Column(db.Integer, db.ForeignKey('Game.id'), nullable=False)
    vendor = db.Column(db.Integer, db.ForeignKey('Vendor.id'), nullable=False)

    # serializer
    def __init__(self, owner, purchased_on, game, vendor):
        self.owner = owner
        self.purchased_on = purchased_on
        self.game = game
        self.vendor = vendor

    def add(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def get(self):
        return {
            'owner': self.owner,
            'purchased_on': self.purchased_on,
            'play_status': self.play_status,
            'game': self.game,
            'vendor': self.vendor
        }


class User(db.Model):
    # pylint: disable=maybe-no-member
    __tablename__ = 'Auth0user'

    id = db.Column(db.String, primary_key=True, nullable=False)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    picture = db.Column(db.String(255), nullable=False, unique=True)

    # relationship
    my_game = db.relationship('MyGame', backref='User', lazy=True, cascade='all, delete-orphan')


class SystemAuthKey(db.Model):
    # pylint: disable=maybe-no-member
    __tablename__ = 'sysAuth0TokenStorage'

    id = db.Column(db.String(200), primary_key=True, nullable=False, default=random_id_generator)
    token = db.Column(db.String, nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return str(f'{self.expiration}')

    def __init__(self, token, expiration):
        self.token = token
        self.expiration = expiration

    def save(self):
        db.session.add(self)
        db.session.commit()
