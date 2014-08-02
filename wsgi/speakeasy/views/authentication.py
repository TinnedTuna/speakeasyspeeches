from flask import Blueprint, render_template, abort
from flask.ext.login import login_required, current_user, login_user, logout_user
import speakeasy
from speakeasy.database import User 
from speakeasy.views.utils import menu
from speakeasy.forms import LoginForm

import datetime


auth = Blueprint('auth', __name__,
        template_folder='templates')

  
@auth.route('/login', methods = ['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form, menu=menu())

@auth.route('/logout')
def logout():
    logout_user()
    flash("You are now logged out.")
    return index()

@auth.route('/authenticate', methods = ['POST'])
def authenticate():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            flash("Error, incorrect username or password")
            return render_template('login.html', title='Login', form=form, menu=menu())
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login was successful for %s' % (repr(user.display_name)))
            return redirect("/index")
        else:
            flash("Error, incorrect username or password")
            return render_template('login.html', title='Login', form=form, menu=menu())
    else:
        flash("Error, incorrect username or password")
        return render_template('login.html', title='Login', form=form, menu=()) 

