from flask.ext.wtf import Form
from wtforms import TextField, PasswordField 
from wtforms.validators import Required

class LoginForm(Form):
    username = TextField('username', validators = [Required()])
    password = PasswordField('password', validators = [Required()])
