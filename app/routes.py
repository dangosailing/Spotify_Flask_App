from flask import (
    render_template,
    flash,
    request,
    redirect,
    url_for,
    session,
)
from flask_login import login_required, login_user, logout_user, current_user
from app.extensions import bp
from app.auth_handler import AuthHandler
from spotipy import Spotify
from spotipy import FlaskSessionCacheHandler
from app.data_processing import list_to_csv, data_plot_to_base64
from app.api_weather_handler import ApiWeatherHandler
from app.utils import validate_pwd
from app.spotify_data_handler import Spotify_Data_Handler
from app.api_spotify_handler import Spotify_Api_Handler


api_weather_handler = ApiWeatherHandler()
sp_data_handler = Spotify_Data_Handler()
auth_handler = AuthHandler()
cache_handler = FlaskSessionCacheHandler(session)
spotify_auth_manager = auth_handler.spotify_auth_manager()
spotify = Spotify(auth_manager=spotify_auth_manager)
spotify_handler = Spotify_Api_Handler(spotify)


# ----------------- Main App Routes -----------------
@bp.route("/")
def index():
    """
    Returns the index template
    """
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handles user login.
    POST = validate user and redirect to Spotify authorization.
    GET = Renders the login page
    """
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
    """
    Handles user registration
    POST= Validate and register the user, then redirect to the login page.
    GET= Render the registration page.
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not validate_pwd(password):
            flash(
                "Password must be at least 6 characters long, contain one upper-case letter and one number"
            )
        elif auth_handler.register(username, password):
            flash("Registration complete. You have been redirected to the login page")
            return redirect(url_for("main.login"))
        else:
            flash("Username already taken!")
    return render_template("register.html")


@bp.route("/logout")
def logout():
    """
    Logout user, clear session data and redirect to index
    """
    logout_user()
    session.clear()

    flash("Logged out!")
    return redirect(url_for("main.index"))


# ----------------- Spotify Routes -----------------
@bp.route("/callback")
def callback():
    """
    Callback for the Spotify API requests. Gets access token to store in session, redirects to home if it works, login if failed
    """
    try:
        token_info = spotify_auth_manager.get_access_token(request.args["code"])
        session["token_info"] = token_info
        if token_info:
            session["token_info"] = token_info
            flash("Authorization succeeded.")
            return redirect(url_for("main.home"))
        else:
            flash("Authorization failed. Please try again.")
            return redirect(url_for("main.login"))
    except:
        flash("Spotify session token not available")
        return redirect(url_for("main.login"))


@bp.route("/home")
@login_required
def home():
    """
    Get home profile for user with recent top artists and tracks. Fetch current weather conditions and display a related track in the embedded player.
    """
    current_weather = api_weather_handler.get_weather_conditions()
    weather_track = spotify.search(q=f"{current_weather}", limit=1, type="track")
    weather_track_id = weather_track["tracks"]["items"][0]["id"]
    user_profile = spotify_handler.get_current_user()
    user_top_artists = spotify_handler.get_top_artists()
    user_top_tracks = spotify_handler.get_top_tracks()
    session["spotify_user_id"] = user_profile["id"]

    return render_template(
        "home.html",
        spotify_profile=user_profile,
        user=current_user,
        top_artists=user_top_artists,
        top_tracks=user_top_tracks,
        current_weather=current_weather,
        weather_track_id=weather_track_id,
    )


@bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """
    Search spotify tracks
    POST= Perform search and display results. Track can be added to specified playlist
    GET= Redirect to home page if no search query is found.
    """
    if request.method == "POST":
        user_playlists = spotify_handler.get_current_user_playlists()
        query = request.form["query"]
        session["search_query"] = query
        if len(query) == 0:
            flash("Query left empty")
            return redirect(url_for("main.home"))
        track_data = spotify_handler.search_tracks(query)
        return render_template(
            "search_results.html",
            results=track_data,
            query=query,
            user_playlists=user_playlists,
        )
    flash("No search query found. Try again")
    return redirect(url_for("main.home"))


@bp.route("/artists/<artist_id>")
@login_required
def get_artist(artist_id: str):
    """
    Fetch artist's singles and display them along with a data plot mapping popularity of single releases over time
    """
    artist_singles_data = spotify_handler.get_artist_singles(artist_id)
    filename = f"{artist_id}_singles"
    list_to_csv(artist_singles_data, filename=filename)
    data_plot = data_plot_to_base64(filename, x_col="release", y_col="popularity")
    return render_template(
        "artist.html", data_plot=data_plot, singles_data=artist_singles_data
    )


@bp.route("/playlists")
@login_required
def playlists():
    """
    Get all recent playlists for current user
    """
    user_recent_playlists = spotify_handler.get_current_user_playlists()

    return render_template(
        "playlists.html", user=current_user, playlists=user_recent_playlists
    )


@bp.route("/playlist/unfollow/<playlist_id>")
@login_required
def unfollow_playlist(playlist_id: str):
    """
    Unfollow/Remove playlist and redirect to the playlists page
    """
    spotify_handler.unfollow_playlist(playlist_id)
    flash("Playlist unfollowed")
    return redirect(url_for("main.playlists"))


@bp.route("/playlist/add_track/<track_id>", methods=["POST", "GET"])
@login_required
def add_to_playlist(track_id: str):
    """
    POST:Add track to playlist and redirect to playlist page after adding track
    """
    if request.method == "POST":
        playlist_id = request.form["playlist_id"]
        spotify_handler.add_items_to_playlist(playlist_id, [track_id])
        flash("Item added to playlist!")
        return redirect(url_for("main.playlist", playlist_id=playlist_id))
    return redirect(url_for("main.home"))


@bp.route("/playlist/remove_track/<track_id>", methods=["POST"])
@login_required
def remove_from_playlist(track_id: str):
    """
    POST:Remove a track from a playlist  and redirect to playlist page after removing track
    """
    if request.method == "POST":
        playlist_id = request.form["playlist_id"]
        spotify_handler.remove_item_from_playlist(playlist_id, track_id)
        flash("Item removed from playlist!")
        return redirect(url_for("main.playlist", playlist_id=playlist_id))
    return redirect(url_for("main.home"))


@bp.route("/playlist/<playlist_id>")
@login_required
def playlist(playlist_id: str):
    """
    Renders the playlist tracks
    """
    playlist = spotify_handler.get_playlist(playlist_id)

    return render_template(
        "playlist.html",
        user=current_user,
        playlist_id=playlist_id,
        playlist_owner=playlist["owner"],
        playlist_name=playlist["name"],
        spotify_user_id=session.get("spotify_user_id"),
        tracks=playlist["tracks"],
    )


@bp.route("/playlist/new", methods=["POST"])
@login_required
def new_playlist():
    """
    POST: Create new playlist
    """
    if request.method == "POST":
        name = request.form["name"]
        spotify_user_id = session.get("spotify_user_id")
        spotify_handler.create_new_playlist(spotify_user_id, name)
        flash(
            "New playlist created. Use the search function to populate it with your favorite tracks"
        )
    return redirect(url_for("main.playlists"))


@bp.route("/playlist/save/<playlist_id>")
@login_required
def save_playlist(playlist_id: str):
    """
    Backup the specified playlist to database and redirect to the playlist page
    """

    playlist = spotify_handler.get_playlist(playlist_id)
    sp_data_handler.backup_playlist(playlist=playlist, current_user=current_user)
    flash("Playlist saved to database")
    return redirect(url_for("main.playlist", playlist_id=playlist_id))


@bp.route("/playlist/backups")
@login_required
def get_playlist_backups():
    """
    Display the user's playlist backups
    """
    playlist_backups = sp_data_handler.get_playlist_backups(current_user=current_user)
    return render_template("playlist_backups.html", playlists=playlist_backups)


@bp.route("/playlist/restore/<playlist_id>")
@login_required
def restore_playlist(playlist_id: str):
    """
    Use the backup data to create a new playlist in Spotify and redirect to the playlists page
    """
    playlist_data = sp_data_handler.get_backup_data(playlist_id)
    spotify_user_id = session.get("spotify_user_id")
    playlist_title = playlist_data["title"]
    new_playlist_id = spotify_handler.create_new_playlist(
        spotify_user_id, playlist_title
    )
    spotify_handler.add_items_to_playlist(
        playlist_id=new_playlist_id, track_ids=playlist_data["track_uris"]
    )
    return redirect(url_for("main.playlists"))
