from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, setup_db, Movie, Actor

# setup the app and the database

app = Flask(__name__)
app.app_context().push()
setup_db(app)
