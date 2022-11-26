import os
import base64
from flask import url_for, jsonify
from src import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from src import login
from src.upload import upload_file
from src.flaskModels.paginate import PaginatedAPIMixin

UserRoles = db.Table('userRoles', db.Model.metadata,
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
    )


class User(db.Model, UserMixin, PaginatedAPIMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), index=True, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    created_up = db.Column(db.DateTime(), nullable=True)
    password_hash = db.Column(db.String(128))
    authenticated = db.Column(db.Boolean, default=False)
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    phone = db.Column(db.String(20), nullable=True)
    roles = db.relationship('Role', secondary=UserRoles,
        primaryjoin=(UserRoles.c.user_id == id),
        secondaryjoin=(UserRoles.c.role_id == id),
        backref = db.backref('users', lazy = 'dynamic'),lazy = 'dynamic')
    last_seen = db.Column(db.DateTime(), default = datetime.utcnow)
    about_me = db.Column(db.String(140), nullable=True)
    image = db.Column(db.String(140))

    def __repr__(self):
        return self.username 

    def upload(self, file):
        fileneme = upload_file(file,'users')
        if filename is False:
            return False
        self.image = filename

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds = expires_in )
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds - 1)
    
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_followers(id):
        pass

    def to_dict(self, include_email=False):
        role = self.roles.filter(UserRoles.c.user_id == self.id)
        data = {
            'id': self.id,
            'username': self.username,
            'firstname': self.first_name,
            'lastname': self.last_name,
            'email': self.email,

            # 'last_seen': self.last_seen.isoformat() + 'Z',
            # 'about_me': self.about_me,
            # 'post_count': self.posts.count(),
            # 'follower_count': self.followers.count(),
            # 'followed_count': self.followed.count(),
            # '_links': {
            #     'self': url_for('api.get_user', id=self.id),
            #     'followers': url_for('api.get_followers', id=self.id),
            #     'followed': url_for('api.get_followed', id=self.id),
            #     'avatar': self.avatar(128)
            # }
        }
        if role is None:
            data['roles'] = role
        else:
            data['roles'] = {}
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'first_name', 'last_name']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def users_role(self):
        return self.query.join(
            UserRoles, (UserRoles.c.user_id == self.id)).order_by(
                    self.timestamp.desc())


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), unique=True, default='role_user')
    # users = db.relationship('User', secondary='userRoles', backref=db.backref("roles", lazy="dynamic"))

    def __repr__(self):
        return self.name 



    

