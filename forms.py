"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

from models import Band


class SignupForm(FlaskForm):
    """User Sign-up Form."""
    username = StringField(
        'Username',
        validators=[
            Length(min=5),
            DataRequired()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=6, message='Select a stronger password.')
        ]
    )
    confirm = PasswordField(
        'Confirm Your Password',
        validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ]
    )
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """User Log-in Form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class EditForm(FlaskForm):
    editarea = TextAreaField('Bands', render_kw={'class': 'form-control', 'rows': 30, 'cols': 50,
                                                 'style': 'overflow: scroll; white-space: pre'})
    editsubmit = SubmitField('Save')

    def fill_area(self, bands):
        bands_str_list = ['\t'.join([str(band.id), band.name, band.tags, str(band.rating), band.url])
                          for band in bands]
        bands_str = '\n'.join(bands_str_list)
        self.editarea.data = bands_str

    def parse_bands(self, user):
        bands_str = self.editarea.data
        bands_str_list = bands_str.split('\n')
        bands = []
        for band in bands_str_list:
            tokens = [t.strip() for t in band.split('\t')]
            bands.append(Band(id=int(tokens[0]),
                              name=tokens[1],
                              tags=tokens[2],
                              rating=float(tokens[3]),
                              url=tokens[4],
                              user_id=user.id))
        return bands


class PlayForm(FlaskForm):
    engineselect = RadioField('Engine',
                              choices=[('default', 'default'), ('spotify', 'Spotify'), ('youtube', 'Youtube')],
                              default='default')
    playsubmit = SubmitField('Let\'s rock!')
