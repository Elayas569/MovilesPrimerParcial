from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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


@products_bp.route("/<int:barcode>", methods=["PUT"])
@jwt_required()
def update(barcode):
    current_user = get_jwt_identity()
    claims = get_jwt()
    current_user_is_admin = claims.get('isAdmin', False)
    
    data = request.get_json()
    
    product = Products.query.filter_by(barcode=barcode).first()
    if not current_user_is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403
    else:
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        else:
            product.name = data['name']
            product.buyPrice = data['buyPrice']
            product.sellPrice = data['sellPrice']
            product.stock = data['stock']
            if 'marca' in data and data['marca'] is not None:
                product.marca = data['marca']
            if 'imageUrl' in data and data['imageUrl'] is not None:
                product.imageUrl = data['imageUrl']
            db.session.commit()
            return jsonify({'message': 'Product updated'}), 200