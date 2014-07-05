from flask import render_template, flash, redirect
from flask.ext.login import login_user, current_user, login_required
from forms import LoginForm, CreatePage
from app import db, app, lm, models, bcrypt
import datetime

@app.route('/')
@app.route('/index')
def index():
    user = current_user
    return render_template("index.html", user=user)

@app.route('/blog')
def blog():
    user = { 'username' :'blogUser' }
    posts = [
            { 
                'author' : 'Frank',
                'title' : 'First Post!',
                'content' : 'This is the very first post!'
                },
            {
                'author' : 'Sally',
                'title' : 'Another Post!',
                'content' : 'This is also a post!'
                }
            ]
    return render_template("blog.html", user=user, posts=posts, title="Blog")

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
        return render_template('view_page.html', page=page)
    

@lm.user_loader
def user_loder(id):
    return models.User.query.get(int(id))
