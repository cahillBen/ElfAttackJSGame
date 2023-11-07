from wtforms import SubmitField, StringField
from flask_wtf import FlaskForm
from wtforms.validators import InputRequired, EqualTo, NumberRange

class UsernameForm(FlaskForm):
    username = StringField("Choose a Username:", validators=[InputRequired()])
    submit = SubmitField("Submit")
