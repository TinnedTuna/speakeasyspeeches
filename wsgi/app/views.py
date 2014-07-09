from flask import render_template, flash, redirect, url_for, abort, g
from flask.ext.login import login_user, current_user, login_required, logout_user
from forms import LoginForm, CreatePage, BlogPost, UserForm
from app import db, app, lm, models, bcrypt
import datetime

@app.route('/')
@app.route('/index')
def index():
    return view_page(1)

@app.before_request
def before_request():
    g.user = current_user

@app.route('/blog/<id>')
def view_blog_post(id):
    post = models.Blog.query.get(id)
    if post is None:
        abort(404)
    else:
        return render_template("view_blog.html", user=current_user, \
                menu=menu(blog_menu_location()), post=post, title=post.title)

@app.route('/blog/post/<id>', methods=['GET'])
@login_required
def show_edit_post(id):
    post = models.Blog.query.get(id)
    form = BlogPost()
    if post is None:
        abort(404)
    form.title.data = post.title
    form.content.data = post.content
    return render_template("edit_blog.html", form=form, user=current_user,\
            menu=menu(blog_menu_location()), post=post, post_id=post.id, \
            title="Editing %s" %(post.title))

@app.route('/blog/post/<id>', methods=['POST'])
@login_required
def edit_post(id):
    post = models.Blog.query.get(id)
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
        return view_blog_post(new_post.id)
    else:
        flash("Could not validate input, please try again")
        return show_create_blog_post() 

@app.route('/blog/post', methods=['GET'])
@login_required
def show_create_blog_post():
    form = BlogPost()
    return render_template('edit_blog.html', title='Create Blog', form=form, menu=menu(blog_menu_location()))

@app.route('/blog', methods=['GET'])
def show_blog():
    all_posts = models.Blog.query.order_by(models.Blog.timestamp.desc())
    return render_template('blog_overview.html', title='Blog', posts=all_posts, menu=menu(blog_menu_location()))

@app.route('/login', methods = ['GET'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form, menu=menu())

@app.route('/logout')
def logout():
    logout_user()
    flash("You are now logged out.")
    return index()

@app.route('/authenticate', methods = ['POST'])
def authenticate():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
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
            return render_template('index.html', user=current_user, menu=menu())
        else:
            flash('Could not create page, a page with that title already exists')
            return render_template('edit_page.html', form=form, menu=menu())

@app.route('/page/edit/<id>', methods = ['GET'])
@login_required
def show_edit_page(id):
    form = CreatePage()
    page = models.Page.query.get(int(id))
    if page is None:
        abort(404)
    else:
        form.title.data = page.title
        form.content.data = page.content
        return render_template('edit_page.html', form=form, page_id=page.id, menu=menu(page.id))

@app.route('/page/edit/<id>', methods= ['POST'])
@login_required
def edit_page(id):
    form = CreatePage()
    existing_page = models.Page.query.get(int(id))
    if existing_page is None:
        abort(404)
    else:
        existing_page.title=form.title.data
        existing_page.content = form.content.data
        db.session.add(existing_page)
        db.session.commit()
        flash("Page updated")
        return render_template('view_page.html', page=existing_page, title=existing_page.title, menu=menu(page.id), user=current_user)

@app.route('/page/create', methods = ['GET'])
@login_required
def show_create_page():
    form = CreatePage()
    return render_template('edit_page.html', form=form, menu=menu())

@app.route('/page/<id>', methods = ['GET'])
def view_page(id):
    page = models.Page.query.get(int(id))
    if page is None:
        abort(404)
    else:
        return render_template('view_page.html', page=page, menu=menu(page.id), title=page.title)

@app.route('/user/create', methods=['GET'])
@login_required
def show_create_user():
    form = UserForm()
    return render_template('edit_user.html', menu=menu(), form=form)

@app.route('/user/edit/<id>', methods=['GET'])
@login_required
def show_edit_user(id):
    user = models.User.query.get(id)
    if user is None:
        abort(404)
    else:
        form = UserForm()
        form.username.data = user.username
        form.display_name.data = user.display_name
        return render_template('edit_user.html', menu=menu(), form=form, user_id=user.id)

@app.route('/user/create', methods=['POST'])
@login_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash("Cannot create a user with that username, one already exists.")
            return show_create_user()
        if form.new_password.data is None or form.new_password.data == "":
            flash("A user requires a password.")
            return show_create_user()
        new_user = models.User()
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

@app.route('/user/edit/<id>', methods=['POST'])
@login_required
def edit_user(id):
    existing_user = models.User.query.get(id)
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
        db.session.commit()
        flash("User update was successful")
        return users() 

@app.route('/users', methods=['GET'])
@login_required
def users():
    users = models.User.query.all()
    return render_template("view_users.html", menu=menu(), users=users, title="Users")


@app.route('/buy')
def buy():
    return view_page(1)

@app.route('/contact')
def contact():
    return view_page(1)

@lm.user_loader
def user_loder(id):
    return models.User.query.get(int(id))

def menu(active_id=None):
    pages = models.Page.query.order_by(models.Page.id)
    menu = []
    for page in pages:
        menu_item = { 'menu_display' : page.title, \
                'menu_url' : url_for('view_page', id=page.id)}
        if active_id is not None:
            menu_item["active"] = active_id == page.id
        menu.append(menu_item)
    contact_page = {
            'menu_display' : 'Contact',\
            'menu_url' : url_for('contact')}
    blog_page = {
            'menu_display' : 'Blog', \
            'menu_url' : url_for('show_blog')}
    if (active_id == len(menu) + 1):
        contact_page["active"] = True
    if (active_id == len(menu) + 2):
        blog_page["active"] = True
    menu.append(contact_page)
    menu.append(blog_page)
    return menu
                
def blog_menu_location():
    return len(models.Page.query.all()) + 2

@app.errorhandler(404)
def handle404(error):
    return render_template("404.html", menu=menu())

@app.errorhandler(401)
def handle401(error):
    return render_template("401.html", menu=menu())
