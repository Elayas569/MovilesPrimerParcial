from flask import Flask
from config.db import init_db, db
from routes.users import users_bp
from routes.health import health_bp
from routes.products import products_bp
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()  # Carga las variables del .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
if os.getenv('FLASK_ENV') == 'development':
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=30)
    print("App started in production")
if os.getenv('FLASK_ENV') == 'production':
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)

init_db(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(health_bp, url_prefix='/health')
app.register_blueprint(products_bp, url_prefix='/products')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
