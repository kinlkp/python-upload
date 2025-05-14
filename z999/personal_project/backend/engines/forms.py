from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    name = StringField('Search host (e.g. hh\d+)', validators=[DataRequired()])
    submit = SubmitField('Submit')