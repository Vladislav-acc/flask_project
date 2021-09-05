from . import db
from flask import current_app
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from hashlib import md5
from tzlocal import get_localzone
import pytz
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(10))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    admin = db.Column(db.Boolean, default=False)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime(timezone=True), default=func.now())
    avatar = db.Column(db.String(50), default=None)
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')
    likes = db.relationship('Like', backref='user')

    def __repr__(self):
        return f"User {self.username}"

    def set_admin(self):
        self.admin = True
        return f"{self.username} теперь новый админ!"

    def take_admin(self):
        self.admin = False
        return f"{self.username} больше не админ!"

    def get_avatar(self, size):
        if self.avatar:
            return f'/static/avatars/{self.username}_{self.avatar}'
        else:
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

    def get_reset_token(self, expires_sec=600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(400), nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', passive_deletes=True)
    likes = db.relationship('Like', backref='post', passive_deletes=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(200), nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'), nullable=False)