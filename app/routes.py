from flask import (
    render_template,
    flash,
    request,
    redirect,
    url_for,
    session,
)
from pprint import pp
from flask_login import login_required, login_user, logout_user, current_user
from app.extensions import bp
from app.auth_handler import AuthHandler
from spotipy import Spotify
from spotipy import FlaskSessionCacheHandler

auth_handler = AuthHandler()
cache_handler = FlaskSessionCacheHandler(session)
spotify_auth_manager = auth_handler.spotify_auth_manager()
spotify = Spotify(auth_manager=spotify_auth_manager)


# ----------------- Main App Routes -----------------
@bp.route("/")
def index():
    flash("Welcome to my Spotify App!")
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = auth_handler.validate_user(username, password)
        if user:
            login_user(user)
            auth_url = spotify_auth_manager.get_authorize_url()
            return redirect(auth_url)
        else:
            flash("Invalid login attempt!")
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if auth_handler.register(username, password):
            flash("Registration complete. You have been redirected to the login page")
            return redirect(url_for("main.login"))
        else:
            flash("Username already taken!")
    return render_template("register.html")


@bp.route("/logout")
def logout():
    logout_user()
    session.clear()

    flash("Logged out!")
    return redirect(url_for("main.index"))


# ----------------- Spotify Routes -----------------
@bp.route("/callback")
@login_required
def callback():
    """Callback for the Spotify API requests"""
    token_info = spotify_auth_manager.get_access_token(request.args["code"])
    session["token_info"] = token_info
    if token_info:
        session["token_info"] = token_info
        flash("Authorization succeeded.")
        return redirect(url_for("main.home"))
    else:
        flash("Authorization failed. Please try again.")
        return redirect(url_for("main.login"))


@bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    user_profile = spotify.current_user()
    user_top_artists = spotify.current_user_top_artists()
    user_top_tracks = spotify.current_user_top_tracks()
    session["spotify_user_id"] = user_profile["id"]
    spotify_profile = {
        "id": user_profile["id"],
        "followers": user_profile["followers"]["total"],
        "href": user_profile["href"],
        "image_src": user_profile["images"],
    }

    top_artists = []

    for artist in user_top_artists["items"]:
        top_artists.append(
            {
                "id": artist["id"],
                "name": artist["name"],
                "followers": artist["followers"]["total"],
                "genres": ", ".join(artist["genres"]),
                "href": artist["external_urls"]["spotify"],
                "image_src": artist["images"][0]["url"],
            }
        )

    top_tracks = []
    for track in user_top_tracks["items"]:
        top_tracks.append(
            {
                "id": track["id"],
                "name": track["name"],
                "artists": track["artists"],
                "popularity": track["popularity"],
                "href": track["external_urls"]["spotify"],
                "image_src": track["album"]["images"][0]["url"],
            }
        )

    return render_template(
        "home.html",
        spotify_profile=spotify_profile,
        user=current_user,
        top_artists=top_artists,
        top_tracks=top_tracks,
    )


@bp.route("/playlists", methods=["GET", "POST"])
@login_required
def playlists():
    user_recent_playlists = spotify.current_user_playlists()
    playlists = []
    for playlist in user_recent_playlists["items"]:
        playlists.append(
            {
                "id": playlist["id"],
                "name": playlist["name"],
                "href": playlist["external_urls"]["spotify"],
            }
        )
    return render_template("playlists.html", user=current_user, playlists=playlists)


@bp.route("/playlist/<playlist_id>", methods=["GET", "POST"])
@login_required
def playlist(playlist_id: str):
    """Display playlist tracks with GET, remove tracks using POST requests"""
    if request.method == "POST":
        track_id = request.form["track_id"]
        playlist_position = request.form["playlist_position"]
        flash(f"{track_id} {playlist_position}")
        response = spotify.user_playlist_remove_all_occurrences_of_tracks(
            user=session.get("spotify_user_id"),
            playlist_id=playlist_id,
            tracks=[{"uri": track_id, "positions": [playlist_position]}],
        )
        flash(response)

    playlist = spotify.playlist(playlist_id=playlist_id)
    playlists_tracks = []
    for track in playlist["tracks"]["items"]:
        playlists_tracks.append(
            {
                "id": track["track"]["id"],
                "name": track["track"]["name"],
                "popularity": track["track"]["popularity"],
                "uri": track["track"]["uri"],
            }
        )
    playlist_owner = playlist["owner"]["id"]
    return render_template(
        "playlist.html",
        user=current_user,
        playlist_id=playlist_id,
        playlist_owner=playlist_owner,
        playlist_name=playlist["name"],
        spotify_user_id=session.get("spotify_user_id"),
        tracks=playlists_tracks,
    )
