from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


# album search form
class AlbumSearchForm(FlaskForm):
    album = StringField("Enter Album Name", validators=[DataRequired()])
    submit = SubmitField("Search For This Album")


# artist search form
class ArtistSearchForm(FlaskForm):
    name = StringField("Enter Artist Name", validators=[DataRequired()])
    submit = SubmitField("Search For This Artist")
