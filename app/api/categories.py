from flask import jsonify
from ..models import Category
from . import api


@api.route('/categories/')
def get_categories():
    """Get all categories available."""

    categories = Category.query.all()
    return jsonify({
        'categories': [category.to_json() for category in categories]
    })


@api.route('/categories/<int:id>')
def get_category(id):
    """Get a category's info given its id."""

    category = Category.query.get_or_404(id)
    return jsonify(category.to_json())
