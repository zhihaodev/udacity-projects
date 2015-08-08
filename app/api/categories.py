from flask import jsonify
from ..models import Category
from . import api


@api.route('/categories/')
def get_categories():
    categories = Category.query.all()
    return jsonify({
        'categories': [category.to_json() for category in categories]
    })


@api.route('/categories/<int:id>')
def get_category(id):
    category = Category.query.get_or_404(id)
    return jsonify(category.to_json())


@api.route('/categories/<name>')
def get_category_by_name(name):
    category = Category.query.filter_by(name=name).first_or_404()
    return jsonify(category.to_json())
