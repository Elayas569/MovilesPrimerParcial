from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models.product import Products
from config.db import db

products_bp = Blueprint('products', __name__)


@products_bp.route("/register", methods=["POST"])
def register():
    # data
    return
