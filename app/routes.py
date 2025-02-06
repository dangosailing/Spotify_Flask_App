from flask import render_template, flash, request, redirect, url_for, session
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
    response = spotify.current_user()
    spotify_profile = {
        "followers": response["followers"]["total"],
        "id": response["id"],
        "href": response["href"],
        "image_src": response["images"][0]["url"],
    }
    return render_template(
        "home.html", spotify_profile=spotify_profile, user=current_user
    )
