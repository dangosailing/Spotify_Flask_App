from app.extensions import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_playlist = db.Table(
    "user_playlist",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("playlist_id", db.String(100), db.ForeignKey("playlist.spotify_id")),
)

playlist_track = db.Table(
    "playlist_track",
    db.Column("playlist_id", db.Integer, db.ForeignKey("playlist.spotify_id")),
    db.Column("track_id", db.String(100), db.ForeignKey("track.spotify_id")),
)

artist_track = db.Table(
    "artist_track",
    db.Column("artist_id", db.Integer, db.ForeignKey("artist.spotify_id")),
    db.Column("track_id", db.String(100), db.ForeignKey("track.spotify_id")),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    following = db.relationship(
        "Playlist", secondary=user_playlist, backref="following"
    )

    def __repr__(self):
        return f"User('{self.username}')"


class Playlist(db.Model):
    spotify_id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    tracks = db.relationship("Track", secondary=playlist_track, backref="tracks")

    def __repr__(self):
        return f"Playlist('{self.title}')"


class Artist(db.Model):
    spotify_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    features = db.relationship("Track", secondary=artist_track, backref="features")

    def __repr__(self):
        return f"Artist('{self.title}')"

class Track(db.Model):
    spotify_id = db.Column(db.String(100), primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Track('{self.title}')"

