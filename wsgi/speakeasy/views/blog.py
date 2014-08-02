from flask import Blueprint, render_template, abort
from flask.ext.login import login_required, current_user
import speakeasy
from speakeasy.database import Blog
from speakeasy.views.utils import menu, blog_menu_location

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
                menu=menu(blog_menu_location()), post=post, title=post.title)

@blog.route('/')
def view_blog():
    posts = Blog.query.all()
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
        db.session.add(post)
        db.session.commit()
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
        db.session.add(new_post)
