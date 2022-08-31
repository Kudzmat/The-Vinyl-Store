from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class AlbumSearchForm(FlaskForm):
    album = StringField("Enter Album Name", validators=[DataRequired()])
    submit = SubmitField("Search For This Album")


class ArtistSearchForm(FlaskForm):
    name = StringField("Enter Artist Name", validators=[DataRequired()])
    submit = SubmitField("Search For This Artist")

