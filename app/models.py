from app.extensions import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_playlist = db.Table("user_playlist", 
    db.Column(db.Integer, db.ForeignKey("user.id")),
    db.Column(db.Integer, db.ForeignKey("playlist.id"))
    spotify_id = db.Column(db.String(100))
    )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    following = db.relationship("Playlist", secondary=user_playlist, backref="followers")

    def __repr__(self):
        return f"User('{self.username}')"

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User('{self.title}')"

