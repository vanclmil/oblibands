"""Logged-in page routes."""
from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required, logout_user

from app import db
from forms import EditForm, PlayForm

# Blueprint Configuration
from models import Band, BAND_STATES

from numpy.random import choice

main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@main_bp.route('/', methods=['GET'])
@login_required
def dashboard():
    bands = Band.query.filter_by(user_id=current_user.id).all()

    bandsform = EditForm(BAND_STATES['approved'])
    bandsform.fill_area([b for b in bands if b.state == BAND_STATES['approved']])

    newbandsform = EditForm(BAND_STATES['queued'])
    newbandsform.fill_area([b for b in bands if b.state == BAND_STATES['queued']])

    playform = PlayForm()

    return render_template(
        'dashboard.jinja2',
        title='Oblibands',
        template='dashboard-template',
        current_user=current_user,
        playform=playform,
        bandsform=bandsform,
        newbandsform=newbandsform
    )


@main_bp.route('/edit', methods=['POST'])
@login_required
def edit():
    bandsform = EditForm(BAND_STATES['approved'])
    if bandsform.validate_on_submit():
        try:
            edited_bands = bandsform.parse_bands(current_user)
            edited_bands = [db.session.merge(band) for band in edited_bands]
            to_delete_bands = [b for b in current_user.bands
                               if b.state == BAND_STATES['approved'] and b not in edited_bands]
            for b in to_delete_bands:
                db.session.delete(b)
            db.session.commit()
            bandsform.fill_area(edited_bands)
        except:
            flash('Cannot save, respect the input format!')
    else:
        raise Exception('Should not happend')

    newbandsform = EditForm(BAND_STATES['queued'])
    newbandsform.fill_area([b for b in current_user.bands if b.state == BAND_STATES['queued']])

    playform = PlayForm()

    return render_template(
        'dashboard.jinja2',
        title='Oblibands',
        template='dashboard-template',
        current_user=current_user,
        playform=playform,
        bandsform=bandsform,
        newbandsform=newbandsform
    )


@main_bp.route('/queue', methods=['POST'])
@login_required
def queue():
    bandsform = EditForm(BAND_STATES['approved'])
    bandsform.fill_area([b for b in current_user.bands if b.state == BAND_STATES['approved']])

    newbandsform = EditForm(BAND_STATES['queued'])
    if newbandsform.validate_on_submit():
        try:
            edited_bands = newbandsform.parse_bands(current_user)
            edited_bands = [db.session.merge(band) for band in edited_bands]
            to_delete_bands = [b for b in current_user.bands
                               if b.state == BAND_STATES['queued'] and b not in edited_bands]
            for b in to_delete_bands:
                db.session.delete(b)
            db.session.commit()
            newbandsform.fill_area(edited_bands)
        except:
            flash('Cannot save, respect the input format!')
    else:
        raise Exception('Should not happend')

    playform = PlayForm()

    return render_template(
        'dashboard.jinja2',
        title='Oblibands',
        template='dashboard-template',
        current_user=current_user,
        playform=playform,
        bandsform=bandsform,
        newbandsform=newbandsform
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
            tags_string = playform.tagsbox.data
            new_bands = playform.queueselect.data
    else:
        engine_name = request.args.get('engine', default='default', type=str)
        tags_string = request.args.get('tags', type=str)
        new_bands = request.args.get('newbands', type=bool)
    engine = SUPPORTED_ENGINES.get(engine_name, DefaultEngine)
    tags = [t.strip() for t in tags_string.split(';') if t.strip() != '']

    if new_bands:
        bands = Band.query.filter_by(user_id=current_user.id, state=BAND_STATES['queued']).all()
    else:
        bands = Band.query.filter_by(user_id=current_user.id, state=BAND_STATES['approved']).all()

    if tags:
        bands = [b for b in bands if any(t in b.tags for t in tags)]

    if not bands:
        flash('Nothing to play!')
        return redirect(url_for('main_bp.dashboard'))

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
