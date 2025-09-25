from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint('health', __name__)


@health_bp.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "message": "Server is running my bro",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }), 200
