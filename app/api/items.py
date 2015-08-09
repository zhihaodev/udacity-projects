from flask import jsonify
from ..models import Item, Category
from . import api


@api.route('/items/')
def get_items():
    """Get all items available."""

    items = Item.query.all()
    return jsonify({
        'items': [item.to_json() for item in items]
    })


@api.route('/items/<int:id>')
def get_item(id):
    """Get an item's info given its id."""

    item = Item.query.get_or_404(id)
    return jsonify(item.to_json())


@api.route('/categories/<int:id>/items/')
def get_category_items(id):
    """Get all items given its category id."""

    category = Category.query.get_or_404(id)
    return jsonify({
        'items': [item.to_json() for item in category.items]
    })


@api.route('/categories/by_name/<name>/items/')
def get_category_items_by_name(name):
    """Get all items given its category name."""

    category = Category.query.filter_by(name=name).first_or_404()
    return jsonify({
        'items': [item.to_json() for item in category.items]
    })
