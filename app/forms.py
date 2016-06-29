from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class LoginForm(Form):
    email = StringField('email', validators = [DataRequired()])
    password = StringField('password', validators = [DataRequired()])

class AccountCreate(Form):
    account_name = StringField('email', validators = [DataRequired()])
    counter_id = StringField('email', validators = [DataRequired()])
    goal_id = StringField('email', validators = [DataRequired()])
    token = StringField('email', validators = [DataRequired()])

class AccountEdit(Form):
    account_name = StringField('email', validators = [DataRequired()])
    counter_id = StringField('email', validators = [DataRequired()])
    goal_id = StringField('email', validators = [DataRequired()])
    token = StringField('email', validators = [DataRequired()])


    
