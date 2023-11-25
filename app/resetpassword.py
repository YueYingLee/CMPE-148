from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class ResetForm(FlaskForm):
 username = StringField('Username',validators =[DataRequired(), Length (min = 6, max = 15)], render_kw ={"placeholder":"Username"})
 password = PasswordField('New Password', validators = [DataRequired(), Length (min=4, max =10)], render_kw ={"placeholder":"Password"})
 confirm = PasswordField ('Confirm password', validators = [DataRequired(), EqualTo('password',message='password does not match')], render_kw ={"placeholder":"Confirm Password"})
 submit = SubmitField ("Reset")
