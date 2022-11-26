from flask import url_for
from src import db
from datetime import datetime, timedelta
from src.flaskModels.paginate import PaginatedAPIMixin

from src.flaskModels.usersModel import User
from src.flaskModels.categoryModel import Category

class Plat(db.Model, PaginatedAPIMixin):
    __tablename__ = 'plats'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text(), nullable = True)
    price = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime(), default = datetime.utcnow)
    created_up = db.Column(db.DateTime(), nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category')

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'category': Category.query.get(self.category_id).to_dict() or {},
            'user': User.query.get(self.user_id).to_dict() or {}
        }
        return data

    def from_dict(self, data, up=False):
        for field in ['name', 'description', 'price', 'category_id']:
            if field in data:
                setattr(self, field, data[field])
            self.user = User.query.get(data['user_id']) 
            self.category = Category.query.get(data['category_id']) 
            if up:
                self.created_up = datetime.utcnow()

