from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt
from models.movement import Movements
from models.product import Products
from config.db import db

movements_bp = Blueprint("movements", __name__)


@movements_bp.route("/all", methods=["GET"])
@jwt_required()
def getAllMovements():
    try:
        claims = get_jwt()
        current_user_is_admin = claims.get("isAdmin", False)
        if current_user_is_admin:
            movements = Movements.query.all()
            movements_list = []
            for movement in movements:
                movements_list.append(
                    {
                        "id": movement.id,
                        "barcode": movement.barcode,
                        "user_id": movement.user_id,
                        "user_name": movement.user.name,
                        "quantity": movement.quantity,
                        "timestamp": movement.timestamp,
                        "notes": movement.notes,
                    }
                )
            return jsonify(movements_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@movements_bp.route("/<int:barcode>", methods=["GET"])
@jwt_required()
def get_movements_per_product(barcode):
    try:
        claims = get_jwt()
        current_user_is_admin = claims.get("isAdmin", False)
        if current_user_is_admin:
            product = Products.query.filter_by(barcode=barcode).first()
            if not product:
                return jsonify({"message": "Product not found"}), 404
            movements = Movements.query.filter_by(barcode=barcode)
            if not movements:
                return (
                    jsonify({"message": "Movements with that barcode not found"}),
                    404,
                )
            movements_list = []
            for movement in movements:
                movements_list.append(
                    {
                        "id": movement.id,
                        "barcode": movement.barcode,
                        "user_id": movement.user_id,
                        "user_name": movement.user.name,
                        "quantity": movement.quantity,
                        "timestamp": movement.timestamp,
                        "notes": movement.notes,
                    }
                )
        return jsonify(movements_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
