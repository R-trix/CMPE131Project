from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, StringField, PasswordField, SubmitField, FileField, FormField
from flask_login import current_user
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.widgets.core import TextArea
from flask_wtf.file import FileField, FileRequired, FileAllowed


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

    username = StringField("Enter your username", validators=[DataRequired()])
    email = StringField("Enter your email", validators=[DataRequired()])

    password = PasswordField("Enter your password", validators=[DataRequired()])
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


class FlashCardForm(FlaskForm):
    term = StringField('Term', validators=[DataRequired()])
    definition = StringField('Definition', validators=[DataRequired()])

    submit = SubmitField("Submit")
    
    
class UploadForm(FlaskForm):
    file = FileField()


class SearchForm(FlaskForm):
    text = StringField("Please enter the text you would like to search for in the flashcards.", validators=[DataRequired()])
    submit = SubmitField("Find the Flashcard")
 

class PracticeForm(FlaskForm):
    ans = StringField('Answer', validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class ShuffleForm(FlaskForm):
    shuffle = SubmitField("Shuffle!")


class NotesForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    
    submit = SubmitField("Add Note")

<<<<<<< HEAD
class ShareFlashCardsForm(FlaskForm):
    user = StringField('Enter the user you want to share with', validators=[DataRequired()])
    submit = SubmitField("Share FlashCards!")

=======
class ShareForm(FlaskForm):
    user = StringField("Send to this user", validators=[DataRequired()])
    notes = SelectField("Notes")
    
    submit = SubmitField("Submit")
>>>>>>> 874b545e53929cb376325632a122c0490e6b07fd
"""
class MailForm(FlaskForm):
    file = FileField("Upload File", validators=[FileRequired(), FileAllowed(['pdf', 'md'], "You can only upload .pdf and .md files.")])
    submit = SubmitField("Upload File and Send as an Email.")    
    """
""" 
<form action="/" method="POST">
        <input type="text" name="content" id="content">
        <input type="submit" value="Add Task">
</form>
"""
