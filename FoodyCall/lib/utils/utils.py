from flask import Flask
from flask import Blueprint
# Create Blueprint
utils = Blueprint('utils', __name__, template_folder='templates')

@utils.route('/utils')
def utils():
    return "utils go here"