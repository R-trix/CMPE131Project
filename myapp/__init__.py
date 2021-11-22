from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'
from flask_login import LoginManager

import os
basedir = os.path.abspath(os.path.dirname(__file__))

#create Flask class object named  myobj
myobj = Flask(__name__)

myobj.config.from_mapping(
	SECRET_KEY = 'you-will-know',
	#location of sqlite databse
	SQLALCHEMT_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
	SQLALCHEMY_TRACK_MODIFICATIONS = False
)


db = SQLAlchemy(myobj)

login = LoginManager(myobj)
#right side is function which  gets called to login  users
login.login_view = 'login'



from myapp import routes
