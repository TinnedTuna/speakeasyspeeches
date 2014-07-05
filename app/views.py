from flask import render_template, flash, redirect
from flask.ext.login import login_user, current_user
from forms import LoginForm
from app import app, lm, models, bcrypt

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

@lm.user_loader
def user_loder(id):
    return models.User.query.get(int(id))
