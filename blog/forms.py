from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models import User
# very cool, define your own form objects
# validators save you a big head ache as well
#  {{ form.username.label(class="form-control-label") }} is possible because we inherite from (flaskform)
class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValueError("Username already in use. Please Try another")
    def validate_email(self,email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValueError("Email already in use. Please Try another")

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    # when you enter these on the html template, the first field "Title" is the label... the data type is StringField
    title = StringField('Title', validators=[DataRequired()] )
    # textAreaField is the large text datatype for SQL
    content = TextAreaField('content', validators=[DataRequired()])
    submit = SubmitField('Post it!')

class TaskForm(FlaskForm):
    # notice that you don't include things like the ID or something like that
    content = StringField('new task', validators=[DataRequired()])
    submit = SubmitField('Add Task!')
    # add due date as an optional field

    #add a feature so that you can insert a new task anywhere in the list