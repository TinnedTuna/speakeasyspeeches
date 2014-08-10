from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask.ext.login import login_required, current_user
import speakeasy
from speakeasy.database.models import Blog, db_session
from speakeasy.forms import BlogPost
from speakeasy.views.utils import menu, blog_menu_location, site_config


import datetime

blog = Blueprint('blog', __name__,
        template_folder='templates', url_prefix='/blog')

@blog.route('/<id>')
def view_blog_post(id):
    post = Blog.query.get(id)
    if post is None:
        abort(404)
    else:
        return render_template("view_blog.html", user=current_user, \
                menu=menu(blog_menu_location()), post=post, title=post.title, \
                site_config=site_config())

@blog.route('/')
def view_blog():
    posts = Blog.query.order_by(Blog.timestamp.desc()).all()
    return render_template('blog_overview.html', user=current_user, \
            menu=menu(blog_menu_location()), posts=posts, title="Blog",\
            site_config=site_config())

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
            title="Editing %s" %(post.title), \
            site_config=site_config())

@blog.route('/post', methods=['GET'])
@login_required
def show_create_post():
    form = BlogPost() 
    return render_template("edit_blog.html", form=form, \
            user=current_user, menu=menu(blog_menu_location()), site_config=site_config())

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
                user=current_user, menu=menu(blog_menu_location()), site_config=site_config())
