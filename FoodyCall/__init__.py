from flask import Flask
from lib.menu.menu import menu
from lib.ratings.ratings import ratings
from lib.order.order import order

app = Flask(__name__)

# Initialize blueprints
app.register_blueprint(menu, url_prefix='/menu')
app.register_blueprint(ratings, url_prefix='/ratings')
app.register_blueprint(order, url_prefix='/order')
@app.route('/')
def login():
    return "Enter your cell # here!"

if __name__ == '__main__':
    app.run()
