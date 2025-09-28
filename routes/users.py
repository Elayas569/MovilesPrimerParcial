from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from models.user import Users
from config.db import db

users_bp = Blueprint("users", __name__)
bcrypt = Bcrypt()


@users_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if Users.query.filter_by(email=data["email"]).first():
            return jsonify({"message": "Email already registered"}), 400
        hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        user = Users(
            name=data["name"],
            email=data["email"],
            password=hashed_pw,
            isAdmin=data.get("isAdmin", False),
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@users_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user = Users.query.filter_by(email=data["email"]).first()
        if user and bcrypt.check_password_hash(user.password, data["password"]):
            access_token = create_access_token(
                identity=str(user.id), additional_claims={"isAdmin": user.isAdmin}
            )
            return jsonify(access_token=access_token), 200
        return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route("/all", methods=["GET"])
@jwt_required()
def getAllUsers():
    try:
        claims = get_jwt()
        current_user_is_admin = claims.get("isAdmin", False)
        if current_user_is_admin:
            users = Users.query.all()
            users_list = []
            for user in users:
                users_list.append(
                    {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "password": user.password,
                        "isAdmin": user.isAdmin,
                    }
                )
            return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def modifyUser(id):
    try:
        claims = get_jwt()
        current_user_is_admin = claims.get("isAdmin", False)
        current_user_id = claims.get("id")

        if not (current_user_is_admin or (current_user_id != id)):
            return jsonify({"message": "Admin privileges required"}), 403

        data = request.get_json() or {}
        user = Users.query.filter_by(id=id).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        if "name" in data:
            user.name = data["name"]
        if "email" in data:
            if Users.query.filter_by(email=data["email"]).first():
                return jsonify({"message": "Email already registered"}), 400
            user.email = data["email"]
        if "password" in data:
            hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
            user.password = hashed_pw
        if "isAdmin" in data and current_user_is_admin:
            user.isAdmin = data["isAdmin"]

        db.session.commit()
        return (
            jsonify(
                {
                    "message": "User updated",
                    "user": {
                        "id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "isAdmin": user.isAdmin,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
