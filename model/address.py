from controller.sql_alchemy import db

class AddressModel(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    address_public_id = db.Column(db.String(80), nullable=False, unique=True)
    federal_unity = db.Column(db.String(2), nullable=False)
    postal_code = db.Column(db.String(9), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    district = db.Column(db.String(64), nullable=False)
    street = db.Column(db.String(256), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.BigInteger, nullable=False)

    user_public_id = db.Column(db.String(80), db.ForeignKey('user.public_id'), nullable=False)