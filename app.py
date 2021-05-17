import dotenv
from flask import Flask
from dotenv import load_dotenv
from flask import Blueprint
from flask_cors import CORS
from flask_login import LoginManager, login_manager
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

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')

@app.route('/')
def hello():
    return 'hi, app is running'

@app.route('/test')
def test():
    return 'testing route'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
