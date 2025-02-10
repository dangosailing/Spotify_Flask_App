from app.models import User, Playlist
from app.extensions import db
from flask_login import current_user
from flask import flash

class ApiHandler:
    def create_playlist(self, playlist:dict, current_user = current_user) -> None:
        user = User.query.filter_by(id=current_user.id).first()
        if user:
            if not Playlist.query.filter_by(spotify_id=playlist["id"]).first():
                new_playlist = Playlist(spotify_id=playlist["id"], title=playlist["name"])
                db.session.add(new_playlist)
                user.following.append(new_playlist)
                db.session.commit()
            else:
                flash("PLAYLIST ALREADY EXISTS")
        else:
            flash("USER NOT FOUND")
    
    def get_playlist_backups(self, current_user = current_user) -> list[dict]:
        """ Return user playlists saved to database """
        user = User.query.filter_by(id=current_user.id).first()
        playlist_backups = []
        if user:
            user_playlists = user.following
            for playlist in user_playlists:
                playlist_backups.append(
                    {"id": playlist.spotify_id,
                    "title": playlist.title}
                )
                
            return playlist_backups
        else:
            return None

