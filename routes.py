"""Logged-in page routes."""
from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user, login_required, logout_user

from app import db
from forms import EditForm, PlayForm

# Blueprint Configuration
from models import Band

from numpy.random import choice

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    bandsform = EditForm()
    bands = Band.query.filter_by(user_id=current_user.id).all()
    bandsform.fill_area(bands)

    playform = PlayForm()

    return render_template(
        'dashboard.jinja2',
        title='Oblibands',
        template='dashboard-template',
        current_user=current_user,
        playform=playform,
        bandsform=bandsform
    )


@main_bp.route('/edit', methods=['POST'])
@login_required
def edit():
    bandsform = EditForm()
    if bandsform.validate_on_submit():
        bands = bandsform.parse_bands(current_user)
        bands = [db.session.merge(band) for band in bands]
        to_delete_bands = [band for band in current_user.bands if band not in bands]
        for band in to_delete_bands:
            db.session.delete(band)
        db.session.commit()
    else:
        bands = Band.query.filter_by(user_id=current_user.id).all()
    bandsform.fill_area(bands)

    playform = PlayForm()

    return render_template(
        'dashboard.jinja2',
        title='Oblibands',
        template='dashboard-template',
        current_user=current_user,
        playform=playform,
        bandsform=bandsform
    )


class SpotifyEngine:
    BASE_LINK = "https://open.spotify.com/search/"

    @classmethod
    def completeUrl(cls, band):
        return cls.BASE_LINK + band.name


class YoutubeEngine:
    BASE_LINK = "https://www.youtube.com/results?search_query="

    @classmethod
    def completeUrl(cls, band):
        escaped_name = band.name.replace(" ", "+")
        return cls.BASE_LINK + escaped_name


class DefaultEngine(YoutubeEngine):
    @classmethod
    def completeUrl(cls, band):
        if band.url:
            return band.url
        return super().completeUrl(band)


SUPPORTED_ENGINES = {
    'default': DefaultEngine,
    'spotify': SpotifyEngine,
    'youtube': YoutubeEngine
}


@main_bp.route('/play', methods=['GET', 'POST'])
@login_required
def play():
    if request.method == 'POST':
        playform = PlayForm()
        if playform.validate_on_submit():
            engine_name = playform.engineselect.data
    else:
        engine_name = request.args.get('engine', default='default', type=str)
    engine = SUPPORTED_ENGINES.get(engine_name, DefaultEngine)

    bands = Band.query.filter_by(user_id=current_user.id).all()
    ratings = [b.rating for b in bands]
    total = sum(ratings)
    probabilities = [r / total for r in ratings]
    band = choice(bands, 1, p=probabilities)[0]

    return redirect(engine.completeUrl(band))


@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('auth_bp.login'))
