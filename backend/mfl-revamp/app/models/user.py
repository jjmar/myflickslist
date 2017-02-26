from app import db, bcrypt
from app.models.list import DefaultList, FavList

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

from datetime import date, datetime


class Friendship(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    active = db.Column(db.Integer, default=0)

    def activate_friendship(self):
        self.active = 1
        db.session.commit()


class User(db.Model):

    # Account Specific
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    pw_hash = db.Column(db.String(128), nullable=False)
    verified = db.Column(db.Boolean(), default=False)

    # Profile Specific
    fav_genre = db.Column(db.String(64))
    join_date = db.Column(db.Date(), default=date.today)
    last_online = db.Column(db.DateTime(), default=datetime.utcnow)
    gender = db.Column(db.String(64))
    location = db.Column(db.String(64))
    website = db.Column(db.String(64))
    about = db.Column(db.String(256))
    profile_views = db.Column(db.Integer(), default=0)

    friends = db.relationship('Friendship', primaryjoin=id==Friendship.user_id, lazy='dynamic')  # M:M

    profile_comments = db.relationship('Comment', foreign_keys='Comment.host_id')  # 1:M
    posted_comments = db.relationship('Comment', foreign_keys='Comment.author_id', backref='author')  # 1:M

    default_list = db.relationship('DefaultList', backref='owner', uselist=False)  # 1:1
    fav_list = db.relationship('FavList', backref='owner', uselist=False)  # 1:1
    custom_lists = db.relationship('CustomList', backref='owner')  # 1:M

    recommendations = db.relationship('Recommendation', backref='author')  # 1:M
    reviews = db.relationship('Review', backref='author')  # 1:M

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.default_list = DefaultList(name='Default Movie List')
        self.favourites_list = FavList(name='Favourite Movies')

    @classmethod
    def verify_confirmation_token(cls, token):
        serializer = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = serializer.loads(token)
            user_id = data.get('user_id_confirm')
        except:
            return None

        return User.query.get(user_id)

    @classmethod
    def verify_reset_password_token(cls, token):
        serializer = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = serializer.loads(token)
            user_id = data.get('user_id_reset_pass')
        except:
            return None

        return User.query.get(user_id)

    def set_password(self, password):
        self.pw_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password)

    def generate_confirm_token(self):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['JWT_CONFIRM_TOKEN_EXPIRES'])
        return serializer.dumps({'user_id_confirm': self.id})

    def generate_reset_password_token(self):
        serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=current_app.config['JWT_RESET_PASS_TOKEN_EXPIRES'])
        return serializer.dumps({'user_id_reset_pass': self.id})

    def add_friend(self, friend, active=0):
        self.friends.append(Friendship(user_id=self.id, friend_id=friend.id, active=active))
        db.session.commit()

    def remove_friend(self, friend):
        self.friends.remove(friend)
        friend.friends.remove(self)
        db.session.commit()


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    host_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    body = db.Column(db.String(512))

