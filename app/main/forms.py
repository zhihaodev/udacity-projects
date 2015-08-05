from flask.ext.wtf import Form
from wtforms.validators import Required
from wtforms import StringField, SubmitField, TextAreaField, SelectField


class AddCategoryForm(Form):

    """docstring for AddCategoryForm"""

    name = StringField('Category name', validators=[Required()])
    submit = SubmitField('Submit')


class AddItemForm(Form):

    """docstring for AddItemForm"""

    def __init__(self, categories, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        self.category.choices = [
            (category.id, category.name) for category in categories]

    name = StringField('Item name', validators=[Required()])
    description = TextAreaField('Item description')
    category = SelectField('Category', coerce=int)
    submit = SubmitField('Submit')
