from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from webargs.flaskparser import FlaskParser


db = SQLAlchemy()
migrate = Migrate()
parser = FlaskParser()
