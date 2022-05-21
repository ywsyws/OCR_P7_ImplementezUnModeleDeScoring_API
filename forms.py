from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange, DataRequired


class LoginForm(FlaskForm):
    id = IntegerField(
        "Client ID",
        validators=[DataRequired(), NumberRange(min=1, max=3000)],
    )
    submit = SubmitField("Verify")
