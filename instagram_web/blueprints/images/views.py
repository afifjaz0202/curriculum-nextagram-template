from flask import Blueprint, render_template, request, flash, redirect, Flask, url_for
from werkzeug import secure_filename
from models.image import Image
from instagram_web.util.helpers import upload_file_to_s3
from flask_login import login_required, login_user, current_user

images_blueprint = Blueprint('images',
                            __name__,
                            template_folder='templates')

@images_blueprint.route("/new", methods=['GET'])
def new():
    return render_template('images/new.html')

@images_blueprint.route("/", methods=['POST'])
def create():
    if "user_image" not in request.files:
        flash("No image uploaded!", "danger")
        return redirect(url_for("images.new"))

    file = request.files['user_image']
    file.filename = secure_filename(file.filename)
    image_path = upload_file_to_s3(file, current_user.username)

    image = Image(user_id = current_user.id, image_url = image_path)
    
    if image.save():
        flash("Successfully uploaded image", "success")
        return redirect(url_for("users.show", username = current_user.username))
    else:
        flash("Failed to upload image!", "danger")
        return redirect(url_for("images.new"))
    
@images_blueprint.route("/<id>/show", methods=["GET"])
@login_required
def show(id):
    image = Image.get_or_none(Image.id == id)
    return render_template("images/image_page.html", image = image)