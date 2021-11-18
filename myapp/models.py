from myapp import db
from myapp import login
from flask_login import current_user
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    """
        user DB structure for storing into db
    """

    def __init__(self, username, email, password):
        self.username = username
        self.set_password(password)
        self.email = email
        self.public = True

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    public = db.Column(db.Boolean, index=True)

    password_hash = db.Column(db.String(128))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


""" some stuff goes here"""


@staticmethod
def check_valid_credentials(username, email, password, retypePassword):
    credentials_valid = True
    # what if pass is incorrect?

