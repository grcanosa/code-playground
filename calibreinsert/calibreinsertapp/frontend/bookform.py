

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms import SubmitField

class BookForm(FlaskForm):
    fauthor = StringField("Author",validators=[DataRequired()])
    ftitle = StringField("Title",validators=[DataRequired()])
    fsubmit = SubmitField(label="Add to DataBase!")
