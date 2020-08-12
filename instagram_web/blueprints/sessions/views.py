from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from models.user import User
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from instagram_web.util.google_oauth import oauth

sessions_blueprint = Blueprint("sessions",
                                __name__,
                                template_folder = "templates")

@sessions_blueprint.route("/new", methods=["GET"])
def new():
    return render_template("sessions/new.html")

@sessions_blueprint.route("/", methods=["POST"])
def create():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.get_or_none(User.username == username)
    
    if user:
        if check_password_hash(user.secret_password, password):
            flash("Successfully logged in!", "success")
            login_user(user)
            return redirect(url_for("sessions.show", username = username))
        else:
            flash("Wrong Password!", "danger")
            return redirect(url_for("sessions.new"))
    else:
        flash("Wrong Username!")
        return redirect(url_for("sessions.new"))

@sessions_blueprint.route("/<username>", methods=["GET"])
def show(username):
    user = User.get_or_none(User.username == username)
    return render_template("users/user_page.html", user = user)

@sessions_blueprint.route("/", methods=["GET"])
def index():
    return "SESSIONS"

@sessions_blueprint.route("/<id>/edit", methods=["GET"])
def edit(id):
    pass

@sessions_blueprint.route("/<id>", methods=["POST"])
def update(id):
    pass

@sessions_blueprint.route('/delete', methods=['POST'])
@login_required
def destroy():
    logout_user()
    flash("Logout success!", "success")
    return redirect(url_for("home"))


@sessions_blueprint.route("/google_login")
def google_login():
    redirect_uri = url_for('sessions.authorize', _external = True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route("/authorize/google")
def authorize():
    oauth.google.authorize_access_token()
    email = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo').json()['email']
    user = User.get_or_none(User.email == email)
    if user:
        login_user(user)
        flash("Signed-in Successfully!", "primary")
        return redirect(url_for('users.show',username = user.username))
    else:
        flash("Sign up to continue", "danger")
        return redirect(url_for('users.new'))