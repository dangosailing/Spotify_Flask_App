from spotipy import Spotify


class Spotify_Api_Handler:
    def __init__(self, spotify: Spotify):
        self.spotify = spotify

    def get_current_user(self) -> dict:
        user = self.spotify.current_user()
        spotify_profile = {
            "id": user["id"],
            "followers": user["followers"]["total"],
            "href": user["href"],
            "image_src": user["images"][0]["url"],
        }
        return spotify_profile

    def get_current_user_playlists(self) -> list:
        user_recent_playlists = self.spotify.current_user_playlists()
        playlists_list = []
        for playlist in user_recent_playlists["items"]:
            playlists_list.append(
                {
                    "id": playlist["id"],
                    "name": playlist["name"],
                    "href": playlist["external_urls"]["spotify"],
                    "image_src": (
                        playlist["images"][0]["url"]
                        if playlist["images"] != None
                        else "https://placehold.co/300x300?text=Image+Unavailable"
                    ),
                }
            )
        return playlists_list

    def get_playlist(self, playlist_id: str) -> dict:
        playlist = self.spotify.playlist(playlist_id=playlist_id)
        playlist_name = playlist["name"]
        playlist_owner = playlist["owner"]["id"]
        playlists_tracks = []
        for track in playlist["tracks"]["items"]:
            playlists_tracks.append(
                {
                    "id": track["track"]["id"],
                    "name": track["track"]["name"],
                    "popularity": track["track"]["popularity"],
                    "uri": track["track"]["uri"],
                    "artists": track["track"]["artists"],
                }
            )
        return {
            "id": playlist_id,
            "name": playlist_name,
            "owner": playlist_owner,
            "tracks": playlists_tracks,
        }

    def create_new_playlist(self, spotify_user_id: str, name: str) -> str:
        new_playlist = self.spotify.user_playlist_create(
            user=spotify_user_id, name=name
        )
        return new_playlist["id"]

    def unfollow_playlist(self, playlist_id: str) -> None:
        self.spotify.current_user_unfollow_playlist(playlist_id)

    def add_items_to_playlist(self, playlist_id: str, track_ids: list) -> None:
        self.spotify.playlist_add_items(playlist_id=playlist_id, items=track_ids)

    def remove_item_from_playlist(self, playlist_id: str, track_id: str) -> None:
        self.spotify.playlist_remove_all_occurrences_of_items(
            playlist_id=playlist_id,
            items=[track_id],
        )

    def get_top_artists(self) -> list:
        user_top_artists = self.spotify.current_user_top_artists()
        top_artists_list = []

        for artist in user_top_artists["items"]:
            top_artists_list.append(
                {
                    "id": artist["id"],
                    "name": artist["name"],
                    "followers": artist["followers"]["total"],
                    "genres": ", ".join(artist["genres"]),
                    "href": artist["external_urls"]["spotify"],
                    "image_src": artist["images"][0]["url"],
                }
            )
        return top_artists_list

    def get_top_tracks(self) -> list:
        user_top_tracks = self.spotify.current_user_top_tracks()
        top_tracks_list = []
        for track in user_top_tracks["items"]:
            top_tracks_list.append(
                {
                    "id": track["id"],
                    "name": track["name"],
                    "artists": track["artists"],
                    "popularity": track["popularity"],
                    "href": track["external_urls"]["spotify"],
                    "image_src": track["album"]["images"][0]["url"],
                }
            )
        return top_tracks_list

    def search_tracks(self, query=str) -> list:
        track_data_list = []
        tracks = self.spotify.search(q=query, type="track")
        for track in tracks["tracks"]["items"]:
            track_data_list.append(
                {
                    "id": track["id"],
                    "name": track["name"],
                    "artists": track["artists"],
                    "popularity": track["popularity"],
                    "href": track["external_urls"]["spotify"],
                    "image_src": track["album"]["images"][0]["url"],
                }
            )
        return track_data_list

    def get_artist_singles(self, artist_id: str) -> list:
        # The artist albums request can only net us the track_ids. For the additional data we use the
        # single ids to make a specific request to the get albums endpoint
        artist_singles = self.spotify.artist_albums(
            artist_id=artist_id, include_groups="single", limit=20
        )
        singles_ids = []
        for single in artist_singles["items"]:
            singles_ids.append(single["id"])
        artist_singles_data = self.spotify.albums(singles_ids)
        singles_data_list = []
        for item in artist_singles_data["albums"]:
            singles_data_list.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "popularity": item["popularity"],
                    "release": item["release_date"],
                    "no_tracks": item["total_tracks"],
                }
            )
        return singles_data_list
