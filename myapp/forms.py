from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, PasswordField, SubmitField
from flask_login import current_user
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea


class LoginForm(FlaskForm):
    """ 
        lets users login
    """
    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])

    remember_me = BooleanField('Remember Me')

    submit = SubmitField('Submit')


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


class DeleteForm(FlaskForm):
    """
        this form will allow the users to delete their account if desired
    """

    username = StringField("Enter a username", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired()])

    password = PasswordField("Enter a password", validators=[DataRequired()])
    retypePassword = PasswordField(
        "Please retype your password", validators=[DataRequired()])

    submit = SubmitField("Submit")
    confirm = BooleanField(
        "Are you sure you would like to delete your account permanently?")


class markdown_notes(FlaskForm):
    notes_name = StringField('Name', validators=[DataRequired()])
    note_description = StringField('Note Description', validators=[
                                   DataRequired()], widget=TextArea(), render_kw={'style': 'width: 500px'})
    save_notes = SubmitField('Save Notes')


""" 
<form action="/" method="POST">
        <input type="text" name="content" id="content">
        <input type="submit" value="Add Task">
</form>
"""
