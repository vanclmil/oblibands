"""Database models."""

from sqlalchemy.orm import relationship

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import ForeignKey, Table

from datetime import datetime


class User(UserMixin, db.Model):
    """User account model."""

    __tablename__ = 'user'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.String(200),
        primary_key=False,
        unique=False,
        nullable=False
    )
    bands = relationship("Band")

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


BAND_STATES = {
    'approved': 1,
    'denied': 0,
    'queued': 2
}


class Band(db.Model):
    __tablename__ = 'band'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    user_id = db.Column(
        db.Integer,
        ForeignKey('user.id'),
        primary_key=True
    )
    state = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(200)
    )
    rating = db.Column(
        db.Float,
        nullable=False
    )
    tags = db.Column(
        db.Text
    )
    url = db.Column(
        db.Text
    )


class PlayedBand(db.Model):
    __tablename__ = 'played_band'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        ForeignKey('user.id'),
        primary_key=True
    )
    band_name = db.Column(
        db.String(200)
    )
    url = db.Column(
        db.Text
    )
    date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )


class PlayedTags(db.Model):
    __tablename__ = 'played_tags'
    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        ForeignKey('user.id'),
        primary_key=True
    )
    tags = db.Column(
        db.Text
    )
    date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )
