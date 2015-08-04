from flask.ext.wtf import Form
from wtforms.validators import Required


class AddItemForm(object):

    """docstring for AddItemForm"""

    # def __init__(self, arg):
    #     super(AddItemForm, self).__init__()
    #     self.arg = arg

    name = StringField('name of category', validators=[Required()])
    submit = SubmitField('Submit')
