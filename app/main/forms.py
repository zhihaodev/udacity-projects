from flask.ext.wtf import Form
from wtforms.validators import Required, Length
from wtforms import StringField, SubmitField, TextAreaField, SelectField


class AddCategoryForm(Form):

    """docstring for AddCategoryForm"""

    name = StringField('Category name', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Submit')


class AddOrEditItemForm(Form):

    """docstring for AddItemForm"""

    def __init__(self, categories, *args, **kwargs):
        super(AddOrEditItemForm, self).__init__(*args, **kwargs)
        self.category.choices = [
            (category.id, category.name) for category in categories]

    name = StringField('Item name', validators=[Required(), Length(1, 64)])
    description = TextAreaField('Item description', validators=[Required()])
    category = SelectField('Category', coerce=int)
    submit = SubmitField('Submit')

class DeleteItemForm(Form):
        """docstring for DeleteItemForm"""
        
        submit = SubmitField('Submit')

                
