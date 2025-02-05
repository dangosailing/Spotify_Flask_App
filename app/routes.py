from flask import Blueprint, render_template, flash

bp = Blueprint("main", __name__)


# ----------------- Main App Routes -----------------
@bp.route("/")
def index():
    flash("Welcome to my Spotify App!")
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    return "login"


@bp.route("/register", methods=["GET", "POST"])
def register():
    return "register"


@bp.route("/logout")
def logout():
    return "logout"


# ----------------- Spotify Routes -----------------
