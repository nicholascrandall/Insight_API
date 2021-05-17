import dotenv
from flask import Flask
from dotenv import load_dotenv

load_dotenv()
 
DEBUG = True
PORT = 8000
app = Flask(__name__)

@app.route('/')
def hello():
    return 'hi, app is running'

@app.route('/test')
def test():
    return 'testing route'

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
