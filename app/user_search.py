from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class UserSearch(FlaskForm):
    name = StringField('Search for User', validators=[DataRequired()])
    submit = SubmitField('Chat')