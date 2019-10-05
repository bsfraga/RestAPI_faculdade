from controller.sql_alchemy import db

from model.address import AddressModel

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    public_id = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    admin = db.Column(db.Boolean)

    address = db.relationship(AddressModel, backref='address', lazy=True)

