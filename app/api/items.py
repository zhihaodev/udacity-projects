from flask import jsonify, make_response
from dict2xml import dict2xml as xmlify
from ..models import Item, Category
from . import api


@api.route('/items.json/')
@api.route('/items/')
def get_items():
    """Get all items available using JSON format."""

    items = Item.query.all()
    return jsonify({
        'items': [item.to_dict() for item in items]
    })


@api.route('/items.xml/')
def get_items_xml():
    """Get all items available using XML format."""

    items = Item.query.all()

    response = make_response(xmlify(
        {"item": [item.to_dict('XML') for item in items]},
        wrap="items", indent="  "))
    response.headers["Content-Type"] = "text/xml"
    return response


@api.route('/items.json/<int:id>')
@api.route('/items/<int:id>')
def get_item(id):
    """Get an item's info given its id using JSON format."""

    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict())


@api.route('/items.xml/<int:id>')
def get_item_xml(id):
    """Get an item's info given its id using XML format."""

    item = Item.query.get_or_404(id)
    response = make_response(
        xmlify(item.to_dict('XML'), wrap="item", indent="  "))
    response.headers["Content-Type"] = "text/xml"
    return response


@api.route('/categories/<int:id>/items.json/')
@api.route('/categories/<int:id>/items/')
def get_category_items(id):
    """Get all items given its category id using JSON format."""

    category = Category.query.get_or_404(id)
    return jsonify({
        'items': [item.to_dict() for item in category.items]
    })


@api.route('/categories/<int:id>/items.xml/')
def get_category_items_xml(id):
    """Get all items given its category id using XML format."""

    category = Category.query.get_or_404(id)
    response = make_response(xmlify(
        {"item": [item.to_dict('XML') for item in category.items]},
        wrap="items", indent="  "))
    response.headers["Content-Type"] = "text/xml"
    return response


@api.route('/categories/by_name/<name>/items.json/')
@api.route('/categories/by_name/<name>/items/')
def get_category_items_by_name(name):
    """Get all items given its category name using JSON format."""

    category = Category.query.filter_by(name=name).first_or_404()
    return jsonify({
        'items': [item.to_dict() for item in category.items]
    })


@api.route('/categories/by_name/<name>/items.xml/')
def get_category_items_by_name_xml(name):
    """Get all items given its category name using XML format."""

    category = Category.query.filter_by(name=name).first_or_404()
    response = make_response(xmlify(
        {"item": [item.to_dict('XML') for item in category.items]},
        wrap="items", indent="  "))
    response.headers["Content-Type"] = "text/xml"
    return response
