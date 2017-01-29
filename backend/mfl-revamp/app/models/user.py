from app import db, bcrypt
from app.models.list import DefaultList, FavList
from datetime import date, datetime


friendship = db.Table('friendship', db.Model.metadata,
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True))


class User(db.Model):

    # Account Specific
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(128), unique=True)
    pw_hash = db.Column(db.String(128), nullable=False)

    # Profile Specific
    fav_genre = db.Column(db.String(64))
    join_date = db.Column(db.Date(), default=date.today)
    last_online = db.Column(db.DateTime(), default=datetime.utcnow)
    gender = db.Column(db.String(64))
    location = db.Column(db.String(64))
    website = db.Column(db.String(64))
    about = db.Column(db.String(256))
    profile_views = db.Column(db.Integer(), default=0)

    friends = db.relationship('User', secondary=friendship, primaryjoin=id==friendship.c.user_id,
                              secondaryjoin=id==friendship.c.friend_id)  # M:M

    profile_comments = db.relationship('Comment', foreign_keys='comment.host_id')  # 1:M
    posted_comments = db.relationship('Comment', foreign_keys='comment.author_id', backref='author')  # 1:M

    default_list = db.relationship('DefaultList', backref='owner', uselist=False)  # 1:1
    fav_list = db.relationship('FavList', backref='owner', uselist=False)  # 1:1
    custom_lists = db.relationship('CustomList', backref='owner')  # 1:M

    recommendations = db.relationship('Recommendation', backref='author')  # 1:M
    reviews = db.relationship('Review', backref='author')  # 1:M

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.default_list = DefaultList(name='Default Movie List')
        self.favourites_list = FavList(name='Favourite Movies')

    def set_password(self, password):
        self.pw_hash = bcrypt.generate_password_hash(password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password)


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    host_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    author_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    body = db.Column(db.String(512))
