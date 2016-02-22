"""ORM models"""

from flask import url_for
from . import db
from datetime import datetime
from app import lm
from flask.ext.login import UserMixin


@lm.user_loader
def load_user(id):
    """Callback function required by Flask_Login."""

    return User.query.get(int(id))


class Category(db.Model):

    """Category model"""

    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    items = db.relationship(
        'Item', backref='category', lazy='dynamic',
        cascade='all, delete-orphan')

    def to_dict(self, format='JSON'):
        result = {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id,
            'items': url_for('api.get_category_items',
                             id=self.id, _external=True)
        }
        # Include xml url instead if using xml format
        if format == 'XML':
            result['items'] = url_for('api.get_category_items_xml',
                                      id=self.id, _external=True)
        return result

    def __repr__(self):
        return '<Category %r>' % self.name


class Item(db.Model):

    """Item model"""

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(128))
    img_deletehash = db.Column(db.String(32))
    add_time = db.Column(db.DateTime(), default=datetime.utcnow)

    def to_dict(self, format='JSON'):
        result = {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id,
            'category': url_for('api.get_category',
                                id=self.category_id, _external=True),
            'description': self.description,
            'img_url': self.img_url
        }
        # Include xml url instead if using xml format
        if format == 'XML':
            result['category'] = url_for('api.get_category_xml',
                                         id=self.category_id, _external=True)

        return result

    def __repr__(self):
        return '<Item %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    pic_url = db.Column(db.String(128))
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    add_time = db.Column(db.DateTime(), default=datetime.utcnow)
    categories = db.relationship(
        'Category', backref='owner', lazy='dynamic',
        cascade='all, delete-orphan')
    items = db.relationship(
        'Item', backref='owner', lazy='dynamic',
        cascade='all, delete-orphan')

    def __repr__(self):
        return '<User %r>' % self.name
