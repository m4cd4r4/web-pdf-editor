from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from models.db import db, User

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    try:
        # Create token
        expires = timedelta(hours=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 24))
        access_token = create_access_token(identity=user.id, expires_delta=expires)
        
        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error during login: {e}")
        return jsonify({"error": "Login failed due to an internal error"}), 500

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password or not name:
        return jsonify({"error": "Missing email, password, or name"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email address already registered"}), 409 # 409 Conflict

    try:
        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password_hash=hashed_password, name=name)
        db.session.add(new_user)
        db.session.commit()

        # Create token
        # Consider JWT expiration configuration from app.config
        expires = timedelta(hours=current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES_HOURS", 24))
        access_token = create_access_token(identity=new_user.id, expires_delta=expires)
        
        return jsonify({
            "message": "User registered successfully",
            "token": access_token,
            "user": {
                "id": new_user.id,
                "email": new_user.email,
                "name": new_user.name
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error during registration: {e}")
        return jsonify({"error": "Registration failed due to an internal error"}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_details():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404 # Should not happen if JWT is valid

    return jsonify({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }), 200
