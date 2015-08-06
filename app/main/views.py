from flask import abort, render_template, flash, redirect, url_for, jsonify, request
from . import main
from .. import db
from ..models import Category, Item
from flask.ext.login import login_required
from .forms import AddOrEditItemForm, AddCategoryForm, DeleteItemForm


@main.route('/')
def index():
    categories = Category.query.order_by(Category.name).all()
    return render_template('index.html', categories=categories)


@main.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    form = AddCategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data)
        try:
            db.session.add(new_category)
            db.session.commit()
        except:
            flash(
                ("Failed to add category \"%s\"."
                 " Make sure that the category name is unique.") % new_category.name)
        else:
            flash("A new category \"%s\" has been added." % new_category.name)
        finally:
            return redirect(url_for('.index'))
    return render_template('add_or_edit.html', form=form)


@main.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = AddOrEditItemForm(Category.query.order_by(Category.name).all())
    if form.validate_on_submit():
        new_item = Item(name=form.name.data, description=form.description.data,
                        category=Category.query.get(form.category.data))
        try:
            db.session.add(new_item)
            db.session.commit()
        except:
            flash(
                ("Failed to add item \"%s\"."
                 " Make sure that the item name is unique.") % new_item.name)
        else:
            flash("A new item \"%s\" has been added." % new_item.name)
        finally:
            return redirect(url_for('.index'))

    category_name = request.args.get('category_name')
    if category_name is not None:
        default_category = Category.query.filter_by(name=category_name).first()
        if default_category is None:
            flash("Wrong parameter(s).")
            return redirect(url_for('.index'))
        form.category.data = default_category.id

    return render_template('add_or_edit.html', form=form)


@main.route('/<category_name>/<item_name>', methods=['GET', 'POST'])
def item_info(category_name, item_name):
    item = Item.query.filter_by(name=item_name).first()
    if item is None or item.category.id != category_name:
        abort(404)
    return item.description


@main.route('/<category_name>/<item_name>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(category_name, item_name):

    item = Item.query.filter_by(name=item_name).first()
    if item is None or item.category.name != category_name:
        abort(404)
    form = AddOrEditItemForm(Category.query.order_by(Category.name).all())
    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.category = Category.query.get(form.category.data)

        try:
            db.session.commit()
        except:
            flash(
                ("Failed to edit item \"%s\"."
                 " Make sure that the item name is unique.") % item.name)
        else:
            flash("Item \"%s\" has been edited." % item.name)
        finally:
            return redirect(url_for('.index'))

    form.name.data = item.name
    form.description.data = item.description
    form.category.data = item.category.id
    return render_template('add_or_edit.html', form=form)


@main.route('/<category_name>/<item_name>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(category_name, item_name):
    item = Item.query.filter_by(name=item_name).first()
    if item is None or item.category.name != category_name:
        abort(404)
    form = DeleteItemForm()
    if form.validate_on_submit():
        try:
            db.session.delete(item)
            db.session.commit()
        except:
            flash(("Failed to delete item \"%s\".") % item.name)
        else:
            flash("Item \"%s\" has been deleted." % item.name)
        finally:
            return redirect(url_for('.index'))

    return render_template('delete.html', form=form, item_name=item_name)


@main.route('/<category_name>')
def list_items(category_name):
    category = Category.query.filter_by(name=category_name).first()
    if category is None:
        abort(404)
    return jsonify({'items': [item.to_json() for item in category.items]})
