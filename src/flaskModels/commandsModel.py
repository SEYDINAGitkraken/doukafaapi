from flask import url_for
from src import db
from datetime import datetime, timedelta
from src.flaskModels.paginate import PaginatedAPIMixin
from src.flaskModels.usersModel import User

class Command(db.Model, PaginatedAPIMixin):
    __tablename__ = 'commands'
    created_at = db.Column(db.DateTime(), default = datetime.timedelta.utcnow)
    created_up = db.Column(db.DateTime(), nullable=True)
    commands = db.Column(db.Json(), nullable=False)
    is_valid = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    def to_dict(self):
        data = {
            "id": self.id
            "commands": self.commands,
            "isValid" : self.is_valid,
            "user": User.query.get(self.user_id).to_dict()
        }
        return data

    def from_dict(self, data, up=False):
        for field in ['commands', 'is_valid', 'user_id']:
            if field in data:
                setattr(self, field, data[field])
            self.user = User.query.get(data['user_id']) 
            if up:
                self.created_up = datetime.utcnow()

