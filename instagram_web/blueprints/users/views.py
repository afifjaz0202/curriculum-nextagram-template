from flask import Blueprint, render_template, request, flash, redirect, Flask, url_for
from werkzeug.security import generate_password_hash
from models.user import User
from models.image import Image
from flask_login import login_required, login_user, current_user
from instagram_web.util.helpers import upload_file_to_s3
from werkzeug import secure_filename

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/', methods=['POST'])
def create():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    new_user = User(username = username, email = email, password = password)

    if new_user.save():
        flash("Successfully registered!")
        return redirect(url_for("users.show", username = username))
    else:
        flash(new_user.errors)
        return redirect(url_for("users.new"))


@users_blueprint.route('/<username>', methods=["GET"])
@login_required
def show(username):
    user = User.get_or_none(User.username == username)
    image = Image.get_or_none(Image.user_id == current_user.id)
    
    if user:
        return render_template("users/user_page.html", user = user, image = image)
    else:
        flash(f"No {username} user found.", "danger" )
        return redirect(url_for('home'))
    

@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User.get_or_none(User.id == id)

    if user:
        if current_user.id == int(id):
            return render_template("users/edit.html", user = user)
        else:
            flash("You can't change about other users!", "danger")
            return redirect(url_for("users.show", username = current_user.username))
    else:
        flash("User does not exist!", "danger")
        return redirect(url_for("home"))

@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User.get_or_none(User.id == id)

    if user:
        if current_user.id == int(id):
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")

            user.username = username
            user.email = email

            if len(password) > 0:
                user.password = password

            if user.save():
                flash("Successfully updated!", "success")
                return redirect(url_for("users.show", username = user.username))
            else:
                flash("Update failed!", "danger")
                for error in user.errors:
                    flash(error)
                
                return redirect(url_for("users.edit", id = user.id))
        else:
            flash("You can't change about other users!")
            
            return redirect(url_for("users.show", username = user.username))
    else:
        flash("User does not exist!")
        return redirect(url_for("home"))


@users_blueprint.route('/<id>/upload', methods=['POST'])
@login_required
def upload(id):
    user = User.get_or_none(User.id == id)

    if user:
        if current_user.id == int(id):
            if "profile_image" not in request.files:
                flash("No image uploaded!")
                return redirect(url_for("users.edit", id = id))

            file = request.files["profile_image"]
            file.filename = secure_filename(file.filename)
            image_path = upload_file_to_s3(file, user.username)
            
            user.image_path = image_path
            
            if user.save():
                flash("Successfully uploaded profile image", 'success')
                return redirect(url_for("users.show", username = user.username))

            else:
                flash("Failed to upload image! Please try again", "danger")
                
                return redirect(url_for("users.edit", id = id))
        else:
            flash("You can't change about other users!", "danger")
            return redirect(url_for("users.show", username = user.username))
    else:
        flash("User does not exist!", "danger")
        return redirect(url_for("home"))