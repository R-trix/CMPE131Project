from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
#from flask import random 

import os
basedir = os.path.abspath(os.path.dirname(__file__))

# create Flask class object named  myobj
myobj = Flask(__name__)
Bootstrap(myobj)

myobj.config['MAIL_SERVER'] = 'shiv.gmail.com'
myobj.config['MAIL_PORT'] = 465
myobj.config['MAIL_USERNAME'] = 'group7@gmail.com'
myobj.config['MAIL_PASSWORD'] = 'unsure'
myobj.config["MAIL_USE_TLS"] = False
myobj.config['MAIL_USE_SSL'] = True

mail = Mail(myobj)
myobj.config.from_mapping(
    SECRET_KEY='you-will-know',
    # location of sqlite databse
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(basedir, 'app.db'),
    # SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    # db = SQLAlchemy(myobj)
)


db = SQLAlchemy(myobj)
db.create_all()

login = LoginManager(myobj)
# right side is function which  gets called to login  users
login.login_view = 'login'

from myapp import routes
