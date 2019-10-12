from flask_restful import Resource
from flask import jsonify, request

from model.person import PersonModel, TypePerson
from controller.sql_alchemy import db


class NewPerson(Resource):
    def post(self, public_id):
        data = request.get_json()

        '''
        TODO:
            Adicionar query que valida se informações ja foram inseridas

            - Usar try catch?
        '''

        new_person = None

        if len(data['cpf_cnpj']) > 11:
            new_person = PersonModel(cpf_cnpj=data['cpf_cnpj'],
                                     type_person=TypePerson.PJ,
                                     rg=data['rg'],
                                     user_public_id=public_id)
        else:
            new_person = PersonModel(cpf_cnpj=data['cpf_cnpj'],
                                     type_person=TypePerson.PF,
                                     rg=data['rg'],
                                     user_public_id=public_id)

        db.session.add(new_person)
        db.session.commit()

        return jsonify({'message': 'Successfully registered Person information to an User information'}, {'person': new_person.json()}, {'status code': 201})
