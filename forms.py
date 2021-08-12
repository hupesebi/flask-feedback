from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, NumberRange, Email, Optional
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):

    username = StringField('username', validators = [InputRequired(), Length(min=1, max=20)])
    password = PasswordField('password', validators = [InputRequired(), Length(min=6, max=55)])
    email = StringField('email', validators = [InputRequired(), Email(), Length(max=50)])
    firstname = StringField('firstname', validators = [InputRequired(), Length(max=30)])
    lastname = StringField('lastname', validators = [InputRequired(), Length(max=30)])

class LoginForm(FlaskForm):

    username = StringField('username', validators = [InputRequired(), Length(min=1, max=20)])
    password = PasswordField('password', validators = [InputRequired(), Length(min=6, max=55)])

class FeedbackForm(FlaskForm):

    title = StringField("Title", validators=[InputRequired(message="Title required"), Length(max=100)] )
    content = TextAreaField("Content", validators=[InputRequired(message="Please enter feedback")])