"""Sign-up & log-in forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length

from models import Band, BAND_STATES


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

    def __init__(self, state):
        super(EditForm, self).__init__()
        self.state = state

    def fill_area(self, bands):
        bands_str_list = ['\t'.join([band.name, band.tags, str(band.rating), band.url])
                          for band in bands]
        bands_str = '\n'.join(bands_str_list)
        self.editarea.data = bands_str

    def parse_bands(self, user):
        bands_str = self.editarea.data
        bands_str_list = bands_str.split('\n')
        bands = []
        for i, band in enumerate(bands_str_list):
            tokens = [t.strip() for t in band.split('\t')]

            bands.append(Band(id=i,
                              name=tokens[0],
                              tags=tokens[1],
                              rating=float(tokens[2]),
                              url=tokens[3],
                              user_id=user.id,
                              state=self.state))
        return bands


class PlayForm(FlaskForm):
    engineselect = RadioField('Engine',
                              choices=[('default', 'default'), ('spotify', 'Spotify'), ('youtube', 'Youtube')],
                              default='default')
    tagsbox = StringField('Tags', render_kw={'style': 'width: 100%'})
    playsubmit = SubmitField('Let\'s rock!')
