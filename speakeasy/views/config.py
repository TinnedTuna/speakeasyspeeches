from flask import Blueprint, render_template, flash
from flask.ext.login import login_required, current_user
from speakeasy.database.models import db_session, Page
from speakeasy.forms import ConfigForm 
from speakeasy.views.utils import menu, site_config


config_blueprint = Blueprint('config', __name__,
        template_folder='templates', url_prefix='/config')

@config_blueprint.route('/', methods=['GET'])
@login_required
def view_config():
    form = config_form()
    current_config = site_config()
    form.site_display_name.data = current_config.site_display_name
    form.site_title.data = current_config.site_title 
    form.site_strap_line.data = current_config.site_strap_line
    form.index_page_id.data = current_config.index_page_id
    form.mail_server.data = current_config.mail_server
    form.mail_port.data = current_config.mail_port
    form.mail_username.data = current_config.mail_username
    form.mail_password.data = current_config.mail_password
    form.mail_use_tls.data = current_config.mail_use_tls
    form.mail_enable.data = current_config.mail_enable 
    return render_template("edit_config.html", user=current_user, \
            menu=menu(), title="Edit Site Config", site_config=current_config, form=form)

@config_blueprint.route('/', methods=['POST'])
@login_required
def edit_config():
    form = config_form()
    current_config = site_config()
    if form.validate_on_submit():
        current_config.site_display_name = form.site_display_name.data
        current_config.site_title = form.site_title.data
        current_config.site_strap_line = form.site_strap_line.data
        current_config.index_page_id = form.index_page_id.data
        current_config.mail_server = form.mail_server.data
        current_config.mail_port = form.mail_port.data
        current_config.mail_username = form.mail_username.data
        current_config.mail_password = form.mail_password.data
        current_config.mail_use_tls = form.mail_use_tls.data
        current_config.mail_enable = form.mail_enable.data
        db_session.add(current_config)
        db_session.commit()
        flash("Settings successfully updated")
    else:
        flash("Failed to update settings.")
    return render_template("edit_config.html", user=current_user, \
                menu=menu(), title="Edit Site Config", site_config=current_config, form=form)

def config_form():
    form = ConfigForm()
    form.index_page_id.choices = [(p.id, p.title) for p in Page.query.order_by(Page.id).all()]
    return form

"""
@blog.route('/')

def view_blog():
    posts = Blog.query.order_by(Blog.timestamp.desc()).all()
    return render_template('blog_overview.html', user=current_user, \
            menu=menu(blog_menu_location()), posts=posts, title="Blog")

@blog.route('/post/<id>', methods=['GET'])
@login_required
def show_edit_post(id):
    post = Blog.query.get(id)
    form = BlogPost()
    if post is None:
        abort(404)
    form.title.data = post.title
    form.content.data = post.content
    return render_template("edit_blog.html", form=form, user=current_user,\
            menu=menu(blog_menu_location()), post=post, post_id=post.id, \
            title="Editing %s" %(post.title))

@blog.route('/post', methods=['GET'])
@login_required
def show_create_post():
    form = BlogPost() 
    return render_template("edit_blog.html", form=form, \
            user=current_user, menu=menu(blog_menu_location()))

@blog.route('/post/<id>', methods=['POST'])
@login_required
def edit_post(id):
    post = Blog.query.get(id)
    if post is None:
        abort(404)
    form = BlogPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db_session.add(post)
        db_session.commit()
        flash("Post successfully updated")
    else:
        flash("Failed to update post, failed to validate user input.")
    return show_edit_post(id)

@blog.route('/post', methods=['POST'])
@login_required
def create_blog_post():
    form = BlogPost()
    if form.validate_on_submit():
        new_post = Blog( \
                title = form.title.data, \
                author_user_id=current_user.id, \
                content=form.content.data, \
                timestamp=datetime.datetime.now())
        db_session.add(new_post)
        db_session.commit()
        flash("New blog post successfully posted.")
        return view_blog() 
    else:
        flash("Failed to post, user input validation failed.")
        return render_template("edit_blog.html", form=form, \
                user=current_user, menu=menu(blog_menu_location()))
"""
