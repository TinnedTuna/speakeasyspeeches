from flask import Flask, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.login import LoginManager, current_user

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

@app.route("/")
@app.route("/index")
def index():
    return redirect(url_for("pages.view_page", id=1))
