import os

basedir = os.path.abspath(os.path.dirname(__file__))


SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

if 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
    SQLALCHEMY_DATABASE_URI = os.environ['OPENSHIFT_POSTGRESQL_DB_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository')

CSRF_ENABLED = True

# Hard coded value for testing
SECRET_KEY = "ok0RNUBXEG6n8k4h"

if 'OPENSHIFT_SECRET_TOKEN' in os.environ:
    SECRET_KEY = os.environ['OPENSHIFT_SECRET_TOKEN']

