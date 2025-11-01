from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user

from src.models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    user = User.query.filter_by(username=data.get("username")).first()
    if user and data.get("password") == user.password:
        login_user(user)
        return jsonify({"message": "Logged successfully"})
    return jsonify({"message": "Unauthorized. Invalid username or password"})


@auth_bp.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"message": "Logout successfully"})