from flask import Flask
from lib.menu.menu import menu
from lib.utils.utils import utils
from pymongo import MongoClient
import csv

app = Flask(__name__)

# Initialize blueprints
app.register_blueprint(menu, url_prefix='/menu')
app.register_blueprint(utils, url_prefix='/utils')

@app.route('/')
def login():
    return "Enter your cell # here!"

if __name__ == '__main__':
    app.run()