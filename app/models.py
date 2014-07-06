from app import db
import markdown

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=True)
    display_name = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)
    posts = db.relationship('Blog', backref='author')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return 'User:{id: %r, username: %s}' % (self.id, self.username)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    author_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Post:{id: %r, title: %s}' % (self.id, self.title)

    def rendered_content(self):
        return markdown.markdown(self.content)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    author_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Post:{id: %r, title: %s}' % (self.id, self.title)

    def rendered_content(self):
        return markdown.markdown(self.content)

    def short_content(self):
        return self.rendered_content()[:200]

