from flask import render_template, flash, request, redirect, url_for
from app.extensions import bp
from app.auth_handler import AuthHandler

auth_handler = AuthHandler()

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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if auth_handler.register(username, password):
            flash("Registration complete. You have been redirected to the login page")
            return redirect(url_for("main.login"))
    return render_template("register.html")


@bp.route("/logout")
def logout():
    flash("Logged out!")
    return render_template("index.html")


# ----------------- Spotify Routes -----------------
