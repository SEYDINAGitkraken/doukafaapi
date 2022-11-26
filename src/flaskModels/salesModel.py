from flask import url_for
from src import db
from datetime import datetime, timedelta
from src.flaskModels.paginate import PaginatedAPIMixin
from src.flaskModels.usersModel import User

transaction = db.Table('transactions',
    db.Column('user_sale', db.Integer, db.ForeignKey('user.id')),
    db.Column('user_buy', db.Integer, db.ForeignKey('user.id'))
)

class Sale(db.model, PaginatedAPIMixin):
    __tablename__ = 'commands'
    created_at = db.Column(db.DateTime(), default = datetime.timedelta.utcnow)
    created_up = db.Column(db.DateTime, nullable = True)
    saling = db.Column(db.Json(), nullable = True)
    totals = db.Column(db.Integer, default=0)
    is_fidely = db.Column(db.Boolean, default = False)
    transacted = db.relationship('Sale', secondary=transaction,
        primaryjoin=(transaction.t.user_sale == id),
        secondaryjoin=(transaction.t.user_buy == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def to_dict(self):
        data = {
            "saling":self.saling,
            "totals": self.totals
        }
        return data


    def from_dict(self, data, up=False):
        for field in ['saling', 'totals', 'is_fidely', 'user_id', 'user_sale']:
            if field in data:
                setattr(self, field, data[field])
            self.user.append(User.query.get(data['user_id']))
            self.user.append(User.query.get(data['user_sale']))
            if up:
                self.created_up = datetime.utcnow()
