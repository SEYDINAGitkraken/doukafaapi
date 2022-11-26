

from flask import url_for
from src import db
from datetime import datetime, timedelta
from src.flaskModels.paginate import PaginatedAPIMixin
from src.flaskModels.usersModel import User


class Category(db.Model, PaginatedAPIMixin):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text(), nullable=True)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow())
    created_up = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')

    def from_dict(self, data, up = False):
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])
            self.user = User.query.get(data['user_id']) 
            if up:
                self.created_up = datetime.utcnow()

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user': User.query.get(self.user_id).to_dict()
        }
        return data

