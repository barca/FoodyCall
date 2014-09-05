from flask import Flask
app = Flask(__name__)


@app.route('/')
def FoodyCall():
    return "Hey fatasses!"

if __name__ == '__main__':
    app.run()