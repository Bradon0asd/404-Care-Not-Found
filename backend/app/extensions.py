from flask_smorest import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from webargs.flaskparser import FlaskParser


api = Api()
db = SQLAlchemy()
migrate = Migrate()
parser = FlaskParser()
