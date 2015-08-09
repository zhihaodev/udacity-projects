"""View functions for application's main functionality."""

import requests
from base64 import b64encode
from werkzeug import secure_filename
from flask import abort, render_template, flash, redirect, url_for,\
    jsonify, request, current_app
from flask.ext.login import login_required
from . import main
from .forms import AddOrEditItemForm, AddOrEditCategoryForm, DeleteForm
from .. import db
from ..models import Category, Item
from ..helpers import upload_image, delete_image


@main.route('/')
def index():
    """Render index page."""

    categories = Category.query.order_by(Category.name).all()
    return render_template('index.html', categories=categories)


@main.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    """Render page for adding category."""

    form = AddOrEditCategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data)
        try:
            db.session.add(new_category)
            db.session.commit()
        except:
            flash(
                ("Failed to add category \"%s\"."
                 " Make sure that the category name is unique.")
                % new_category.name)
        else:
            flash("A new category \"%s\" has been added." % new_category.name)
        finally:
            return redirect(url_for('.index'))
    return render_template('add_or_edit.html', form=form)


@main.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    """Render page for adding item."""

    form = AddOrEditItemForm(Category.query.order_by(Category.name).all())
    img_upload_name = None
    if form.validate_on_submit():
        img_upload_name = secure_filename(form.img_upload.data.filename)
        img_deletehash = None
        img_url = None

        # Upload image to Imgur if FileField is specified
        if img_upload_name != '':
            img_url, img_deletehash = upload_image(form.img_upload.data)
            if img_url is None or img_deletehash is None:
                flash("Failed to upload image.")
                return redirect(url_for('.index'))
        elif form.img_url.data != '':
            img_url = form.img_url.data

        new_item = Item(name=form.name.data, description=form.description.data,
                        category=Category.query.get(form.category.data),
                        img_url=img_url, img_deletehash=img_deletehash)

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

    # Set SelectField's default value
    category_name = request.args.get('category_name')
    if category_name is not None:
        default_category = Category.query.filter_by(name=category_name).first()
        if default_category is None:
            flash("Wrong parameter(s).")
            return redirect(url_for('.index'))
        form.category.data = default_category.id

    return render_template('add_or_edit.html',
                           form=form, filename=img_upload_name)


@main.route('/categories/<category_name>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_name):
    """Render page for editing category."""

    category = Category.query.filter_by(name=category_name).first_or_404()
    form = AddOrEditCategoryForm()
    if form.validate_on_submit():
        category.name = form.name.data
        try:
            db.session.commit()
        except:
            flash(
                ("Failed to edit category \"%s\"."
                 " Make sure that the category name is unique.")
                % category.name)
        else:
            flash("Category \"%s\" has been edited." % category.name)
        finally:
            return redirect(url_for('.index'))
    form.name.data = category.name
    return render_template('add_or_edit.html', form=form)


@main.route('/items/<item_name>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_name):
    """Render page for editing item."""

    item = Item.query.filter_by(name=item_name).first_or_404()
    form = AddOrEditItemForm(Category.query.order_by(Category.name).all())
    if form.validate_on_submit():

        img_upload_name = secure_filename(form.img_upload.data.filename)
        img_deletehash = None
        img_url = None

        # Delete uploaded image on Imgur
        if item.img_deletehash is not None \
                and not delete_image(item.img_deletehash):
            flash("Failed to edit item \"%s\"." % item.name)
            return redirect(url_for('.index'))

        # Upload new image on Imgur
        if img_upload_name != '':
            img_url, img_deletehash = upload_image(form.img_upload.data)
            print "img_url: " + img_url
            print "img_deletehash: " + img_deletehash
            if img_url is None or img_deletehash is None:
                flash("Failed to upload image.")
                return redirect(url_for('.index'))

        elif form.img_url.data != '':
            img_url = form.img_url.data

        item.name = form.name.data
        item.description = form.description.data
        item.category = Category.query.get(form.category.data)
        item.img_url = img_url
        item.img_deletehash = img_deletehash

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
    form.img_url.data = item.img_url

    return render_template('add_or_edit.html', form=form)


@main.route('/categories/<category_name>/delete', methods=['GET', 'POST'])
@login_required
def delete_category(category_name):
    """Render page for deleting category."""

    category = Category.query.filter_by(name=category_name).first_or_404()
    form = DeleteForm()
    if form.validate_on_submit():
        try:
            db.session.delete(category)
            db.session.commit()
        except:
            flash(("Failed to delete category \"%s\".") % category.name)
        else:
            flash("Category \"%s\" has been deleted." % category.name)
        finally:
            return redirect(url_for('.index'))
    return render_template('delete.html', form=form, name=category_name)


@main.route('/items/<item_name>/delete', methods=['GET', 'POST'])
@login_required
def delete_item(item_name):
    """Render page for deleting item."""

    item = Item.query.filter_by(name=item_name).first_or_404()
    form = DeleteForm()
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
    return render_template('delete.html', form=form, name=item_name)
