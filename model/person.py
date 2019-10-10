from controller.sql_alchemy import db
from sqlalchemy import Enum


class PersonModel(db.Model):

    __tablename__: 'person'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    cpf_cnpj = db.Column(db.Integer, nullable=False, unique=True)
    type_person = db.Column(db.Enum('PF', 'PJ', name='ValueTypes', default='PF'))
    rg = db.Column(db.Integer, nullable=False, unique=True)

    user_public_id = db.Column(db.String(80), db.ForeignKey(
        'user.public_id'), nullable=False)
