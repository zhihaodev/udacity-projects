from . import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    # description = db.Column(db.Text)
    # add_time = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<Category %r>' % self.name


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    description = db.Column(db.Text)
    add_time = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<Item %r>' % self.name
