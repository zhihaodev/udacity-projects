from flask import jsonify
from ..models import Item, Category
from . import api


@api.route('/items/')
def get_items():
    items = Item.query.all()
    return jsonify({
        'items': [item.to_json() for item in items]
    })


@api.route('/items/<int:id>')
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_json())


@api.route('/items/<name>')
def get_item_by_name(name):
    item = Item.query.filter_by(name=name).first_or_404()
    return jsonify(item.to_json())


@api.route('/categories/<int:id>/items/')
def get_category_items(id):
    category = Category.query.get_or_404(id)
    return jsonify({
        'items': [item.to_json() for item in category.items]
    })
