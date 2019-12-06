from flask_restful import Resource
from flask import jsonify, request, make_response

from model.person import PersonModel, TypePerson
from controller.sql_alchemy import db


class NewPerson(Resource):
    def post(self, public_id):

        try:

            check_data = PersonModel.query.filter_by(
                public_id=public_id).first()

            if check_data.user_public_id:
                return make_response(jsonify({'message': 'Person data already created.'},
                               {'status_code': 400}), 400)

            data = request.get_json()

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
            
        except Exception as ex:
            return make_response(jsonify({'message': f"Something went wrong with the request. Check the parameters and it's values then try again."},
                           {'Exception': f'{ex}'},
                           {'status_code': 500}), 500)
