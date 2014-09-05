from flask import Flask
from lib.menu import menu
from lib.utils import utils
app = Flask(__name__)

# Init blueprints
app.register_blueprint(menu, url_prefix='/menu')
app.register_blueprint(utils, url_prefix='/utils')

@app.route('/')
def login():
    return "Enter your cell # here!"

if __name__ == '__main__':
    app.run()