from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object("config")

bcrypt = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)

import speakeasy.views.utils
from speakeasy.views.pages import pages
app.register_blueprint(pages)

from speakeasy.views.blog import blog
app.register_blueprint(blog)

from speakeasy.views.users import users_blueprint
app.register_blueprint(users_blueprint)

from speakeasy.views.authentication import auth
app.register_blueprint(auth)
print("Application: " + repr(app))
print("Blueprints: " + repr(app.blueprints))
print("View functions: " + repr(app.view_functions))

from speakeasy.database import Page, db_session
