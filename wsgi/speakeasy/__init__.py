from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager
from views import pages

app = Flask(__name__)
app.config.from_object("config")
app.register_blueprint(pages)

bcrypt = Bcrypt(app)
lm = LoginManager()
lm.init_app(app)

