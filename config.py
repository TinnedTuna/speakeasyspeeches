import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, './data/app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

CSRF_ENABLED = True
SECRET_KEY = "ok0RNUBXEG6n8k4h"

