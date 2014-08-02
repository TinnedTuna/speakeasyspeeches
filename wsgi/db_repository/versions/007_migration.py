from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
config = Table('config', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('site_title', Text, nullable=False),
    Column('site_display_name', Text, nullable=False),
    Column('site_strap_line', Text, nullable=False),
    Column('index_page_id', Integer),
    Column('mail_server', Text),
    Column('mail_port', Integer),
    Column('mail_username', Text),
    Column('mail_password', Text),
    Column('mail_use_tls', Boolean),
    Column('mail_enable', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['config'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['config'].drop()
