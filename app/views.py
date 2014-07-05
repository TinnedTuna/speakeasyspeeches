from flask import render_template, flash, redirect
from forms import LoginForm
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = { 'username' : 'Frank!' }
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
        flash("Login requested for " + form.username.data)
        return redirect("/index")
    else:
        flash("Could not validate input!");
        return render_template('login.html', title='Login', form=form)
