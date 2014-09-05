from flask import Blueprint
# Create Blueprint
menu = Blueprint('menu', __name__, template_folder='templates')

@menu.route('')
def index():
    return "Food goes here"