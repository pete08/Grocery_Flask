from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class NewItem(FlaskForm):
    item = StringField('Item Name', validators=[DataRequired()])
    detail = TextAreaField('Detail')
    submit = SubmitField('Post')
