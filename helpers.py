import os

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators


class GameForm(FlaskForm):
    name = StringField('Game name', validators=[validators.DataRequired(), validators.length(min=1, max=50)])
    category = StringField('Category', validators=[validators.DataRequired(), validators.length(min=1, max=40)])
    console = StringField('Console', validators=[validators.DataRequired(), validators.length(min=1, max=50)])
    submit = SubmitField('Submit')


class UserForm(FlaskForm):
    user = StringField('User', validators=[validators.DataRequired(), validators.length(min=1, max=8)])
    password = PasswordField('Password', validators=[validators.DataRequired(), validators.length(min=1, max=100)])
    submit = SubmitField('Submit')


from main import app


def get_image(id):
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if f'thumb-{id}-' in filename:
            return filename
    return 'default_thumb.jpg'


def remove_image(id):
    file = get_image(id)
    if file != 'default_thumb.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], file))
