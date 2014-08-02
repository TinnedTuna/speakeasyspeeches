from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField, SelectField, BooleanField, IntegerField
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])

class CreatePage(Form):
    title = TextField('title', validators = [Required()])
    content = TextAreaField('content', validators= [Required()])

class BlogPost(Form):
    title = TextField('title', validators = [Required()])
    content = TextAreaField('content', validators= [Required()])

class UserForm(Form):
    username = TextField('username', validators = [Required()])
    display_name = TextField('display_name')
    new_password = PasswordField('new_password')
    confirm_password = PasswordField('confirm_password')

class ConfigForm(Form):
    site_display_name = TextField('site_display_name')
    site_title = TextField('site_display_name')
    site_strap_line = TextField('site_display_name')

    index_page_id = SelectField('index_page_id', coerce=int)
    
    mail_server = TextField('mail_server')
    mail_port = IntegerField('mail_port')
    mail_username = TextField('mail_username')
    mail_password = PasswordField('mail_password')
    mail_use_tls = BooleanField('mail_use_tls')
    mail_enable = BooleanField('mail_enable')
