from flask import jsonify, make_response
from dict2xml import dict2xml as xmlify
from ..models import Category
from . import api


@api.route('/categories.json/')
@api.route('/categories/')
def get_categories():
    """Get all categories available using JSON format."""

    categories = Category.query.all()
    return jsonify({
        'categories': [category.to_dict() for category in categories]
    })


@api.route('/categories.xml/')
def get_categories_xml():
    """Get all categories available using XML format."""

    categories = Category.query.all()
    response = make_response(xmlify(
        {"category": [category.to_dict('XML') for category in categories]},
        wrap="categories", indent="  "))
    response.headers["Content-Type"] = "text/xml"
    return response


@api.route('/categories.json/<int:id>')
@api.route('/categories/<int:id>')
def get_category(id):
    """Get a category's info given its id using JSON format."""

    category = Category.query.get_or_404(id)
    return jsonify(category.to_dict())


@api.route('/categories.xml/<int:id>')
def get_category_xml(id):
    """Get a category's info given its id using XML format."""

    category = Category.query.get_or_404(id)
    response = make_response(
        xmlify(category.to_dict('XML'), wrap="category", indent="  "))
    response.headers["Content-Type"] = "text/xml"
    return response
