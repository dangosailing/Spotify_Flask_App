from app.models import User, Playlist, Artist, Track
from app.extensions import db
from flask_login import current_user
from flask import flash


class ApiHandler:
    def create_playlist(self, playlist: dict, current_user: dict) -> None:
        """Creates playlist and appends it to the current user"""
        user = User.query.filter_by(id=current_user.id).first()
        if user:
            if not Playlist.query.filter_by(spotify_id=playlist["id"]).first():
                new_playlist = Playlist(
                    spotify_id=playlist["id"], title=playlist["name"]
                )
                db.session.add(new_playlist)
                user.following.append(new_playlist)
                db.session.commit()
            else:
                flash("Playlist already saved")
        else:
            flash("User not found")

    def save_track_and_artists(self, track: dict) -> None:
        """Save track and featured artists to database and connect them"""
        new_track = Track(
            spotify_id=track["id"], title=track["title"], uri=track["uri"]
        )
        if not Track.query.filter_by(spotify_id=track["id"]).first():
            db.session.add(new_track)
            db.session.commit()
            for artist in track["artists"]:
                if not Artist.query.filter_by(spotify_id=artist["id"]).first():
                    new_artist = Artist(
                        spotify_id=artist["id"],
                        name=artist["name"] if artist["name"] else artist["type"],
                    )
                    db.session.add(new_artist)
                    new_artist.features.append(new_track)
                    db.session.commit()
                else:
                    existing_artist = Artist.query.filter_by(
                        spotify_id=artist["id"]
                    ).first()
                    existing_artist.features.append(new_track)

    def connect_tracks_playlist(self, tracks: list, playlist_id: str) -> None:
        """Save tracks in playlist and connect it to the playlist"""
        playlist = Playlist.query.filter_by(spotify_id=playlist_id).first()
        for track in tracks:
            new_track = Track.query.filter_by(spotify_id=track["id"]).first()
            playlist.tracks.append(new_track)
            db.session.commit()

    def get_playlist_backups(self, current_user=current_user) -> list[dict]:
        """Return user playlists saved to database"""
        user = User.query.filter_by(id=current_user.id).first()
        playlist_backups = []
        if user:
            user_playlists = user.following
            for playlist in user_playlists:
                playlist_backups.append(
                    {
                        "id": playlist.spotify_id,
                        "title": playlist.title,
                        "tracks": playlist.tracks,
                    },
                )
            return playlist_backups
        else:
            return None

    def get_backup_data(self, playlist_id: str) -> dict:
        """Returns the track uri data and playlist title required to populate playlist with tracks"""
        playlist = Playlist.query.filter_by(spotify_id=playlist_id).first()
        playlist_track_uri_list = []
        if playlist:
            tracks = playlist.tracks
            for track in tracks:
                playlist_track_uri_list.append(track.uri)
            return {"track_uris": playlist_track_uri_list, "title": playlist.title}
        else:
            return None

    def backup_playlist(
        self, playlist: dict, current_user: dict = current_user
    ) -> None:
        """Saves a backup of the playlist together with the featured tracks and artists"""
        playlist_id = playlist["id"]
        self.create_playlist(playlist, current_user)
        playlist_tracks = []
        for track in playlist["tracks"]["items"]:
            playlist_tracks.append(
                {
                    "title": track["track"]["name"],
                    "artists": track["track"]["artists"],
                    "id": track["track"]["id"],
                    "uri": track["track"][
                        "uri"
                    ],  # Add items to playlist does not rely on track ids but rather the URI, hence why it´s included here
                }
            )
        for track in playlist_tracks:
            self.save_track_and_artists(track)
        self.connect_tracks_playlist(playlist_tracks, playlist_id)
        return playlist_tracks
