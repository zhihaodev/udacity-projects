"""WTF form classes"""

from flask.ext.wtf import Form
from wtforms.validators import Required, Length, URL, Optional
from wtforms import StringField, SubmitField, TextAreaField, SelectField

from flask_wtf.file import FileField, FileAllowed
from .. import images


class AddOrEditCategoryForm(Form):

    """Form class for adding or editing category."""

    name = StringField('Category name', validators=[Required(), Length(1, 64)])
    submit = SubmitField('Submit')


class AddOrEditItemForm(Form):

    """Form class for adding or editing item."""

    def __init__(self, categories, *args, **kwargs):
        """
        Args:
            categories: all categories available in database

        """

        super(AddOrEditItemForm, self).__init__(*args, **kwargs)
        # Initialize choices the item can have
        self.category.choices = [
            (category.id, category.name) for category in categories]

    name = StringField('Item name', validators=[Required(), Length(1, 64)])
    description = TextAreaField('Item description', validators=[Required()])
    category = SelectField('Category', coerce=int)
    img_url = StringField('Image URL', validators=[Optional(), URL()])
    img_upload = FileField(
        'Or upload image', validators=[FileAllowed(images, 'Images only.')])
    submit = SubmitField('Submit')

    def validate(self):
        """Check if the form submitted is valid."""
        if not super(AddOrEditItemForm, self).validate():
            return False

        # Make sure url field and upload field are not specified
        # at the same time
        if self.img_url.data != '' and self.img_upload.data.filename != '':
            self.img_url.errors.append(
                'Please do not specify image URL '
                'and upload image at the same time.')
            self.img_upload.errors.append(
                'Please do not specify image URL '
                'and upload image at the same time.')
            return False
        return True


class DeleteForm(Form):

    """Form class for deleting."""

    submit = SubmitField('Submit')
