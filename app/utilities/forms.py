from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField,SelectField,TextField,PasswordField,TextAreaField
from wtforms.widgets import HiddenInput,PasswordInput
from wtforms.validators import NumberRange,AnyOf,DataRequired,Length,EqualTo


class SearchForm(FlaskForm):
    page = IntegerField('page', validators=[NumberRange(min=1, message='Page cannot be less than 1.')], default=1, widget=HiddenInput())
    size = IntegerField('size', validators=[AnyOf([50,100], message='Size must be one of: 50, 100.')], default=50, widget=HiddenInput())
    key = StringField('key', default='')
    by = SelectField('by', choices=[('all', 'All'),('actor', 'Actor'),('genre', 'Genre'),('director', 'Director')],
                    validate_choice=False,
                     validators=[AnyOf(['all', 'actor', 'genre', 'director'], message='By muse be one of: all, actor, genre, director.')], default='all')


class LoginForm(FlaskForm):
    username = StringField('UserName', [DataRequired("Enter your name")])
    password = PasswordField('Password', [DataRequired("Enter your password")], widget=PasswordInput(hide_value=False))

class RegisterForm(FlaskForm):
    username = StringField('Your name', [DataRequired('Enter your name.')])
    password = PasswordField('Password', [
        DataRequired("Enter your password"),
        Length(min=6, message="Passwords must be at least 6 characters."),
        EqualTo('confirm', message='Passwords must match')
    ], widget=PasswordInput(hide_value=False))
    confirm = PasswordField('Re-enter Password', [DataRequired("Type your password again")]
                            , widget=PasswordInput(hide_value=False))

class ReviewForm(FlaskForm):
    content = TextAreaField('Content', [DataRequired()])