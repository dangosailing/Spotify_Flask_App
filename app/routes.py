from flask import render_template, flash, request
from app.extensions import bp


# ----------------- Main App Routes -----------------
@bp.route("/")
def index():
    flash("Welcome to my Spotify App!")
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


@bp.route("/logout")
def logout():
    flash("Logged out!")
    return render_template("index.html")


# ----------------- Spotify Routes -----------------
