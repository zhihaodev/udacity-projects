from flask.ext.wtf import Form
from wtforms.validators import Required, Length
from wtforms import StringField, SubmitField, TextAreaField, SelectField


class AddOrEditCategoryForm(Form):

    """docstring for AddOrEditCategoryForm"""

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

class DeleteForm(Form):
        """docstring for DeleteForm"""
        
        submit = SubmitField('Submit')

                
