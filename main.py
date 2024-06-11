from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)
app.config.from_pyfile('config.py')

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from view_game import *
from view_user import *

if __name__ == '__main__':
    app.run(debug=True)
