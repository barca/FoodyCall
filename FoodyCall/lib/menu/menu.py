from flask import Flask
from flask import Blueprint
# Create Blueprint
menu = Blueprint('menu', __name__, template_folder='templates')

@menu.route('/menu')
def menu():
    return "Food goes here"