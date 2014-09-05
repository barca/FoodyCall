from flask import Flask
app = Flask(__name__)


@app.route('/')
def login():
    return "Enter your cell # here!"

@app.route('/menu')
def menu():
    return "Food goes here"

@app.route('/sides')
def sides():
    return "Sides go here"

if __name__ == '__main__':
    app.run()