from flask.ext.wtf import Form
from wtforms import TextField, PasswordField, TextAreaField
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])

class CreatePage(Form):
    title = TextField('title', validators = [Required()])
    content = TextAreaField('content', validators= [Required()])
