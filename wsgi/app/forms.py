from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
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

