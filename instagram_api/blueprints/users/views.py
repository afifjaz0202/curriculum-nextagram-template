from flask import Blueprint, jsonify

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def new():
    return "USERS API"
