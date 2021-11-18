from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, PasswordField, SubmitField
from flask_login import current_user
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    """ 
        lets users login
    """


class RegisterForm(FlaskForm):
    """
        this form will allow users to createa a new account
    """
    username = StringField("Enter a username", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired()])

    password = PasswordField("Enter a password", validators=[DataRequired()])
    retypePassword = PasswordField(
        "Please retype your password", validators=[DataRequired()])

    submit = SubmitField("Submit")

