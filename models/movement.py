from config.db import db


class Movements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.Integer, db.ForeignKey(
        'products.barcode'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())
    notes = db.Column(db.Text)

    # Opcional: relaciones
    product = db.relationship('Products', backref='movements')
    user = db.relationship('Users', backref='movements')
