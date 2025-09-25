from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from models.user import Users
from config.db import db

users_bp = Blueprint('users', __name__)
bcrypt = Bcrypt()


@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = Users(
        name=data['name'],
        email=data['email'],
        password=hashed_pw,
        isAdmin=data.get('isAdmin', False)
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered'}), 201


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Users.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({'message': 'Invalid credentials'}), 401
