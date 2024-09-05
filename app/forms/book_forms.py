from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class BookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    image = StringField('Image URL', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Book')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    # author = StringField('Author', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    submit = SubmitField('Login')


class EditBookForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    image = StringField('Image URL', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Update Book')
