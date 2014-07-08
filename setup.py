from setuptools import setup

setup(name='SpeakEasy-Speeches',
      version='1.0',
      description='SpeakEasy Speeches Website',
      author='Dan Turner',
      author_email='tunafish25@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask==0.10.1',
          'Flask-Bcrypt==0.6.0',
          'Flask-Login==0.2.11',
          'Flask-SQLAlchemy==1.0',
          'Flask-WTF==0.9.5',
          'Jinja2==2.7.3',
          'Markdown==2.4.1',
          'MarkupSafe==0.23',
          'SQLAlchemy==0.9.6',
          'Tempita==0.5.3dev',
          'WTForms==1.0.5',
          'Werkzeug==0.9.6',
          'sqlalchemy-migrate==0.9.1']
     )
