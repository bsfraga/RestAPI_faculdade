from controller.sql_alchemy import db

from model.address import AddressModel
from model.person import PersonModel

class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    public_id = db.Column(db.String(80), nullable=False, unique=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(64), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean)

    #   one to many relationship
    address = db.relationship(AddressModel, backref='address', lazy=True)

    #   one to one relationship
    person_type = db.relationship(PersonModel, lazy=True, backref='user', uselist=False)

    def json(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'username': self.username,
            'email': self.email
        } 

