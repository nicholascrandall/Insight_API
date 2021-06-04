import dotenv
from flask import Flask, after_this_request
from dotenv import load_dotenv
from flask import Blueprint
from flask_cors import CORS
from flask_login import LoginManager
from resources.users import users
import models
import os

load_dotenv()

DEBUG = True
PORT = 8000
app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_APP_SECRET")
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return models.User.get(models.User.id == user_id)

@app.before_request
def before_request():

    """Connect to the db before each request"""
    models.DATABASE.connect()

    @after_this_request
    def after_request(response):
        """Close the db connection after each request"""
        models.DATABASE.close()
        return response

CORS(users, origins=['http://localhost:3000', 'https://insight-nc.herokuapp.com'], supports_credentials=True)

app.register_blueprint(users, url_prefix='/users')

@app.route('/')
def hello():
    return 'hi, app is running'

@app.route('/test')
def test():
    return 'testing route ababa'

@app.route('/stocks/<symbol>')
def show_stock(symbol):
    return "Show page for {}".format(symbol)

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

if os.environ.get('FLASK_ENV') != 'development':
  print('\non heroku!')
  models.initialize()
