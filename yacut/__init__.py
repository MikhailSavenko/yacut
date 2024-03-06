from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from settings import Config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config.from_object(Config)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from . import error_handlers, views, api_views
