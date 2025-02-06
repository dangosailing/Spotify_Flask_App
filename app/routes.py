from flask import render_template, flash, request, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = auth_handler.validate_user(username, password)
        if user:
            login_user(user)
            return redirect(url_for("main.home"))
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
    flash("Logged out!")
    return redirect(url_for("main.index"))


# ----------------- Spotify Routes -----------------
@bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)