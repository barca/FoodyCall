from flask import Blueprint
# Create Blueprint
utils = Blueprint('utils', __name__, template_folder='templates')

@utils.route('')
def index():
    return "utils go here"