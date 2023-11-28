from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_login import current_user
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask import flash
from wtforms.widgets import TextArea


class deleteAcc(FlaskForm):
    password = PasswordField('Enter your password', validators=[DataRequired()])
    submit = SubmitField('Delete Account')

    def validate_password(self, form):
        if not check_password_hash(current_user.password_hash, form.data):
            raise ValidationError('Incorrect password!')
