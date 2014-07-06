from flask import render_template, flash, redirect, url_for
from flask.ext.login import login_user, current_user, login_required
from forms import LoginForm, CreatePage, BlogPost
from app import db, app, lm, models, bcrypt
import datetime

@app.route('/')
@app.route('/index')
def index():
    user = current_user
    return render_template("index.html", user=user, menu=menu())

@app.route('/blog/<id>')
def view_blog_post(id):
    post = models.Blog.query.get(id)
    if post is None:
        ### TODO return 404?
        pass
    else:
        return render_template("view_blog.html", user=current_user, menu=menu(), post=post, title=post.title)

@app.route('/blog/post', methods=['POST'])
@login_required
def create_blog_post():
    form = BlogPost()
    if form.validate_on_submit():
        new_post = models.Blog( \
                title = form.title.data, \
                author_user_id=current_user.id, \
                content=form.content.data, \
                timestamp=datetime.datetime.now())
        db.session.add(new_post)
        db.session.commit()
        return render_template('index.html', user=current_user)
    else:
        flash("Could not validate input, please try again")
        render_template('create_blog.html', title='Create Blog', form=form)

@app.route('/blog/post', methods=['GET'])
@login_required
def show_create_blog_post():
    form = BlogPost()
    return render_template('create_blog.html', title='Create Blog', form=form)

@app.route('/blog', methods=['GET'])
def show_blog():
    all_posts = models.Blog.query.order_by(models.Blog.timestamp)
    return render_template('blog_overview.html', title='Blog', posts=all_posts, menu=menu())

@app.route('/login', methods = ['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is None:
            return render_template('login.html', title='Login', form=form, error=True)
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login was successful for %s' % (repr(user)))
            return redirect("/index")
        else:
            return render_template('login.html', title='Login', form=form, error=True)
    else:
        return render_template('login.html', title='Login', form=form)

@app.route('/page/create', methods = ['POST'])
@login_required
def create_page():
    form = CreatePage()
    if form.validate_on_submit():
        if models.Page.query.filter_by(title=form.title.data).first() is None:
            new_page = models.Page( \
                    title=form.title.data, \
                    author_user_id=current_user.id, \
                    content=form.content.data, \
                    timestamp=datetime.datetime.now())
            db.session.add(new_page)
            db.session.commit()
            return render_template('index.html', user=current_user)
        else:
            flash('Could not create page, a page with that title already exists')
            return render_template('create_page.html', form=form)

@app.route('/page/edit/<id>', methods = ['GET'])
@login_required
def show_edit_page(id):
    form = CreatePage()
    page = models.Page.query.get(int(id))
    if page is None:
        ### TODO return 404
        pass
    else:
        form.title.data = page.title
        form.content.data = page.content
        return render_template('edit_page.html', form=form, page_id=page.id)

@app.route('/page/edit/<id>', methods= ['POST'])
@login_required
def edit_page(id):
    form = CreatePage()
    existing_page = models.Page.query.get(int(id))
    if existing_page is None:
        flash("No such page could be found")
        return render_template('edit_page.html', form=form, page_id=id)
    else:
        existing_page.title=form.title.data
        existing_page.content = form.content.data
        db.session.add(existing_page)
        db.session.commit()
        flash("Page updated")
        return render_template('view_page.html', page=existing_page, title=existing_page.title)

@app.route('/page/create', methods = ['GET'])
@login_required
def show_create_page():
    form = CreatePage()
    return render_template('create_page.html', form=form)

@app.route('/page/<id>', methods = ['GET'])
def view_page(id):
    page = models.Page.query.get(int(id))
    if page is None:
        ### TODO return 404 
        pass
    else:
        return render_template('view_page.html', page=page, menu=menu())
    

@lm.user_loader
def user_loder(id):
    return models.User.query.get(int(id))

def menu():
    index_page = { 
            'menu_display' : 'Home', \
            'menu_url' : url_for('index')
            }
    pages = models.Page.query.order_by(models.Page.id)
    menu = []
    menu.append(index_page)
    for page in pages:
        menu_item = { 'menu_display' : page.title, \
                'menu_url' : url_for('view_page', id=page.id)}
        menu.append(menu_item)
    blog_page = {
            'menu_display' : 'Blog', \
            'menu_url' : url_for('show_blog')}
    menu.append(blog_page)
    return menu
                



