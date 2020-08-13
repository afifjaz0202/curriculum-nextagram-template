from flask import Blueprint,render_template,redirect,url_for,flash, request
from werkzeug import secure_filename
from instagram_web.util.tokens import gateway
from models.relationship import Relationship
from models.user import User
from flask_login import current_user,login_required
import requests
import os

relationships_blueprint = Blueprint("relationships",
                                    __name__,
                                    template_folder="templates")

@relationships_blueprint.route("/new", methods=["GET"])
@login_required
def new():
    return render_template("relationships/new.html")

@relationships_blueprint.route("/", methods=["POST"])
@login_required
def create():
    
    pass