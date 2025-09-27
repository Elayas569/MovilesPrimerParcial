from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.product import Products
from models.user import Users
from models.movement import Movements
from config.db import db

products_bp = Blueprint('products', __name__)
'''
TODO
PENDIENTES
- Error Handling
- Data and Data type validation en las requests
- Todo el docs xd
'''


@products_bp.route("/register", methods=["POST"])
@jwt_required()
def register():
    claims = get_jwt()
    current_user_is_admin = claims.get('isAdmin', False)
    if not current_user_is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403

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
    claims = get_jwt()
    current_user_is_admin = claims.get('isAdmin', False)
    if not current_user_is_admin:
        return jsonify({'message': 'Admin privileges required'}), 403

    data = request.get_json()
    product = Products.query.filter_by(barcode=barcode).first()

    if not product:
        return jsonify({'message': 'Product not found'}), 404

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


@products_bp.route("/<int:barcode>/stock", methods=["PUT"])
@jwt_required()
def updateStock(barcode):
    '''
    Request campos:
    stockAdded int positiva o negativa que se sumará al stock
    notes: informacion de q es, venta, compra, etc
    '''

    current_user_id = get_jwt_identity()
    if not Users.query.get(current_user_id):
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    if "stockAdded" not in data:
        return jsonify({"message": "Missing stock value"}), 400

    try:
        stock_added = int(data["stockAdded"])
    except (ValueError, TypeError):
        return jsonify({"message": "stockAdded must be a number"}), 400

    product = Products.query.filter_by(barcode=barcode).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    product.stock += stock_added

    movement = Movements(
        barcode=barcode,
        user_id=current_user_id,
        quantity=int(data["stockAdded"]),
        notes=data.get('notes', None)
    )
    db.session.add(movement)
    db.session.commit()
    return jsonify({"message": "Stock updated", "new_stock": product.stock}), 200


@products_bp.route("/", methods=["GET"])
@jwt_required()
def list_all_products():
    products = Products.query.all()
    products_list = []
    for product in products:
        products_list.append({
            "barcode": product.barcode,
            "name": product.name,
            "buyPrice": product.buyPrice,
            "sellPrice": product.sellPrice,
            "stock": product.stock,
            "marca": getattr(product, "marca", None),
            "imageUrl": getattr(product, "imageUrl", None)
        })
    return jsonify(products_list), 200


@products_bp.route("/<int:barcode>", methods=["GET"])
@jwt_required()
def get_product(barcode):
    product = Products.query.filter_by(barcode=barcode).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    product_data = {
        "barcode": product.barcode,
        "name": product.name,
        "buyPrice": product.buyPrice,
        "sellPrice": product.sellPrice,
        "stock": product.stock,
        "marca": getattr(product, "marca", None),
        "imageUrl": getattr(product, "imageUrl", None)
    }
    return jsonify(product_data), 200
