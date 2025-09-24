from flask import Flask
from config.db import init_db, db
from routes.users import users_bp
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables del .env

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

init_db(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

app.register_blueprint(users_bp, url_prefix='/users')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)