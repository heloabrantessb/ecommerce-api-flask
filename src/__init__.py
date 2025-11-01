from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from src.controller import register_controller
from src.models import *
from src.database import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    register_controller(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    CORS(app)

    @login_manager.user_loader

    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/')
    def index():
        return 'Hello World!'

    return app