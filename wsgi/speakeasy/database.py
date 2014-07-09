from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Text, \
        ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, backref, relation
from sqlalchemy.ext.declarative import declarative_base

import markdown

from speakeasy import app

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],\
        convert_unicode=true)

db_session = scoped_session(sessionmaker(autocommit=False,\
        autoflush=False,\
        bind=engine))

def init_db():
    Model.metadata.create_all(bind=engine)


Model = declarative_base(name='Model')
Model.query = db_session.query_property()

class User(Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(60), unique=True, nullable=True)
    display_name = Column(Text)
    password = Column(Text, nullable=False)
    posts = relationship('Blog', backref='author')

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

class Page(Model):
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    author_user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return 'Post:{id: %r, title: %s}' % (self.id, self.title)

    def rendered_content(self):
        return markdown.markdown(self.content)

class Blog(Model):
    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False, unique=True)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    author_user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return 'Post:{id: %r, title: %s}' % (self.id, self.title)

    def rendered_content(self):
        return markdown.markdown(self.content)

    def short_content(self):
        return self.rendered_content()[:200]

