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


# playlist request form
class PlaylistForm(FlaskForm):
    artist1 = StringField("First Artist", validators=[DataRequired()])
    artist2 = StringField("Second Artist", validators=[DataRequired()])
    artist3 = StringField("Third Artist", validators=[DataRequired()])
    artist4 = StringField("Fourth Artist", validators=[DataRequired()])
    artist5 = StringField("Fifth Artist", validators=[DataRequired()])
    submit = SubmitField("Check My Vibe!")
