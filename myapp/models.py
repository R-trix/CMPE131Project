from myapp import db
from myapp import login
from flask_login import current_user, UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model, UserMixin):
    """
        user DB structure for storing into db
    """

    def __init__(self, username, email, password):
        """
        parameters:
                email - string: user's email address; gets stored in a coulumn
                username - string: user's chosen username; stored in a column
                password - string: user's password; stored in a column
        """
        self.username = username
        self.set_password(password)
        self.email = email
        self.public = True

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    public = db.Column(db.Boolean, index=True)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    notes = db.relationship('Notes', backref='user', lazy='dynamic')
    cards = db.relationship('FlashCards', backref='user', lazy='dynamic')

    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        """
            this utilizes the werkzeug_security function check_password_hash in order to compare the
            password hash to the password chosen by the user while logging in

            param: password - string: user's entered password to compare to the password provided while logging in which
                   is stored in the databased
        """
        return check_password_hash(self.password_hash, password)

# required props/methods for user obj
# required under flask_login (someone double check that this is correct)
    is_active = True
    is_anonymous = False
    is_aunthenticated = True

    def get_id(self):
        """
             this function is required under the flask_login for users
        """
        return self.id


# some stuff goes here


    @staticmethod
    def check_valid_credentials(username, email, password, retypePassword):
        """
            ensures user's credentials are correct/valid
            params:
                   email - string: ensures unique email
                   username -string: ensures unique un
                   password - string: user's chosen password
                   retypePassword - string: ensure retypePassword and password are both the same/no differences
        """

        credentials_valid = True
        # what if pass is incorrect?

#       if password != retypePassword:
#            credentials_valid=False
        # maybe we should add some kinda popup that tells the user password incorrect

    def set_password(self, password):
        """
            this should enrypt the user's passwork and should store the password hash in the db
            param:
                   password - string:non encrypted password which will get stored in the db
        """
        self.password_hash = generate_password_hash(password)

    @login.user_loader
    def load_user(id):
        """
                [add]
                param: id - int:user's ID to login
                returns: (ser): user obj which is queried from db to login
        """
        return User.query.get(int(id))


class Task(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id
        self.done = False

    def __repr__(self):
        return '<Content %s>' % self.content


class Notes(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.String(512))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, body, user_id):
        self.title = title
        self.body = body
        self.user_id = user_id
    
    def __repr__(self):
        return f'<{self.title}: {self.body}>'


class FlashCards(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(64))
    definition = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, term, definition, user_id):
        self.term = term
        self.definition = definition
        self.user_id = user_id

    def __repr__(self):
        return f'Term: {self.term}, Definition: {self.definition}'

class Timer(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True, unique=True, autoincrement=True)
    username = db.Column(db.String(50))
    pomodoro_interval = db.Column(db.Integer())
    break_interval = db.Column(db.Integer())
    
    
    