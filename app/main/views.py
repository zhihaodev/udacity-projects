from flask import abort, render_template
from . import main
from ..models import Category, Item
from flask.ext.login import login_required


@main.route('/')
def index():
    categories = Category.query.order_by(Category.name).all()
    s = [str((c.id, c.name)) for c in categories]

    return render_template('index.html')


@main.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    pass


@main.route('/<category_name>/<item_name>', methods=['GET', 'POST'])
def item_info():
    item = Item.query.filter_by(name=item_name).first()
    if item is None or item.category.id != category_name:
        abort(404)
    return item.description


@main.route('/<item_name>/edit', methods=['GET', 'POST'])
@login_required
def edit_item():
    pass


@main.route('/<item_name>/delete')
@login_required
def delete_item():
    pass
