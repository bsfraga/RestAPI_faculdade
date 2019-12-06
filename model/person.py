from controller.sql_alchemy import db
from sqlalchemy import Enum
import enum

class TypePerson(enum.Enum):
    PF = 1
    PJ = 2

class PersonModel(db.Model):

    __tablename__: 'person'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    cpf_cnpj = db.Column(db.String(18), nullable=False, unique=True)
    type_person = db.Column(db.Enum(TypePerson))
    rg = db.Column(db.String(18), nullable=False, unique=True)

    user_public_id = db.Column(db.String(80), db.ForeignKey('user.public_id'), nullable=False)

    def json(self):
        return {'cpf_cnpj': self.cpf_cnpj,
                'rg': self.rg,
                'type_person' : self.type_person.name,
                'user_public_id': self.user_public_id}

