from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class ResetForm(FlaskForm):
 username = StringField('Username',validators =[DataRequired(), Length (min = 6, max = 15)], render_kw ={"placeholder":"Username"})
 password = PasswordField('New password', validators = [DataRequired(), Length (min=4, max =10), EqualTo('confirm',message='password does not match')], render_kw ={"placeholder":"New Password"})
 confirm = PasswordField ('Confirm password', validators = [DataRequired(), EqualTo('confirm',message='password does not match')], render_kw ={"placeholder":"Confirm Password"})
 submit = SubmitField ("Reset")
 
 
