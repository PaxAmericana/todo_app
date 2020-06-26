from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__, static_url_path="")
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
# /// three foward slashes means current location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# these are each app extensions, which take the app at the arg
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# do this at the bottom to avoid circular imports
from blog import routes

# trying to delete the one table
# from sqlalchemy import create_engine
# engine = create_engine('sqlite:///site.db', echo=False)
#
# from blog.models import Task
# Task.__table__.drop(engine)