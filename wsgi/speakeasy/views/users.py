from flask import Blueprint, render_template, abort
from flask.ext.login import login_required, current_user
import speakeasy
from speakeasy.database import User 
from speakeasy.views.utils import menu

import datetime

# Named with _blueprint suffic to avoid name collision
# with users() below
users_blueprint = Blueprint('users', __name__,
        template_folder='templates', url_prefix='/user')

@users_blueprint.route('/all', methods=['GET'])
@login_required
def users():
    users = User.query.all()
    return render_template("view_users.html", menu=menu(),\
            users=users, title="Users")

@users_blueprint.route('/edit/<id>', methods=['GET'])
@login_required
def show_edit_user(id):
    user = User.query.get(id)
    if user is None:
        abort(404)
    else:
        form = UserForm()
        form.username.data = user.username
        form.display_name.data = user.display_name
        return render_template('edit_user.html', menu=menu(), form=form, user_id=user.id)

@users_blueprint.route('/create', methods=['POST'])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash("Cannot create a user with that username, one already exists.")
            return show_create_user()
        if form.new_password.data is None or form.new_password.data == "":
            flash("A user requires a password.")
            return show_create_user()
        new_user = User()
        new_user.username = form.username.data
        new_user.display_name = form.display_name.data
        if form.new_password.data != form.confirm_password.data:   
            flash("The supplied passwords did not match.")
            return show_create_user()
        new_user.password = bcrypt.generate_password_hash(form.new_password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("User was created successfully!")
        return render_template('edit_user.html', menu=menu(), form=form, user_id=new_user.id)

@users_blueprint.route('/edit/<id>', methods=['POST'])
@login_required
def edit_user(id):
    existing_user = User.query.get(id)
    if existing_user is None:
        abort(404)
    form = UserForm()
    if form.validate_on_submit():
        existing_user.username = form.username.data
        existing_user.display_name = form.display_name.data
        if form.new_password.data is not None and form.new_password.data != "" and form.new_password.data == form.confirm_password.data:
            new_hash = bcrypt.generate_password_hash(form.new_password.data)
            existing_user.password = new_hash
        db.session.add(existing_user)

