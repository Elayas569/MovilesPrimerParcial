from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models.product import Products
from config.db import db

products_bp = Blueprint('products', __name__)


@products_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if Products.query.filter_by(barcode=data['barcode']).first():
        return jsonify({'message': 'Item already registered'}), 400

    product_data = {
        'barcode': data['barcode'],
        'name': data['name'],
        'buyPrice': data['buyPrice'],
        'sellPrice': data['sellPrice'],
        'stock': data['stock']
    }
    if 'marca' in data and data['marca'] is not None:
        product_data['marca'] = data['marca']
    if 'imageUrl' in data and data['imageUrl'] is not None:
        product_data['imageUrl'] = data['imageUrl']

    product = Products(**product_data)
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Product registered'}), 201
