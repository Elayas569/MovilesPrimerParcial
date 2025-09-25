from config.db import db


class Products(db.Model):
    barcode = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    buyPrice = db.Column(db.Float, nullable=False)
    sellPrice = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    marca = db.Column(db.String(100))
    imageUrl = db.Column(db.String(200))
