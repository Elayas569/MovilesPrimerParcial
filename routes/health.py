from flask import Blueprint, jsonify
from datetime import datetime

health_bp = Blueprint('health', __name__)


@health_bp.route('/', methods=['GET'])
def health_check():
    try:
        return jsonify({
            "message": "Server is running my bro",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "update": "ejemplo video actions"
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
