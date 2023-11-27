from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FormField, FieldList
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    names = StringField('Enter up to 10 usernames seperated by comma below', validators=[DataRequired()])
    submit = SubmitField('Create conversation')
