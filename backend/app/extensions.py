from flask_cors import CORS
from flask_migrate import Migrate
from flask_session import Session
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy


api = Api()
cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
server_session = Session()

