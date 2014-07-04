from flask import render_template
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

