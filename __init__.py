# __init__.py

from flask import Flask
app = Flask(__name__)

from config import Config
app.config.from_object(Config)

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
login_manager = LoginManager()
login_manager.init_app(app)

