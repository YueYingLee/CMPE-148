from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    names = StringField('Enter username(s) seperate by comma', validators=[DataRequired()])
    submit = SubmitField('Create conversation')
