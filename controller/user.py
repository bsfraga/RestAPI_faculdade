import uuid

import jwt
from flask import jsonify, request, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from controller.sql_alchemy import db
from model.address import AddressModel
from model.person import PersonModel
from model.user import UserModel

'''
TODO 1: Validar numero de campos informados na request
TODO 2: Validar se os valores informados nos parâmetros estão corretos

TODO 3: adicionar métodos get
    - exibir valores de person_model
    - validar se isso ainda é necessário
'''


class NewUser(Resource):
    def post(self):

        try:

            '''
            TODO: validar se user informado no cadastro ja existe
            '''

            data = request.get_json()

            already_exists = UserModel.query.filter_by(email=data['email']).first()

            if already_exists:
                return make_response(jsonify({'message': 'The account already exists on the system.'}, {'status_code': 200}), 200)


            hashed_password = generate_password_hash(
                data['password'], method='sha256')

            new_user = UserModel(public_id=str(uuid.uuid4()),
                                 name=data['name'],
                                 username=data['username'],
                                 email=data['email'],
                                 password=hashed_password,
                                 active=True)

            db.session.add(new_user)
            db.session.commit()

            return make_response(jsonify({'message': 'User successfully created.'},
                           {'public_id': new_user.public_id,
                            'name': new_user.name,
                            'username': new_user.username,
                            'email': new_user.email},
                            {'status code': 201}), 201)
        
        except Exception as ex:
            return make_response(jsonify({'message': f"Something went wrong with the request. Check the parameters and it's values then try again."},
                           {'Exception': f'{ex}'},
                           {'status_code': 500}), 500)


class GetUsers(Resource):
    @jwt_required
    def get(self):

        try:

            public_id = get_jwt_identity()
            '''
            TODO: Apenas o bot poderá ter acesso a lista de users
            '''
            # recebe todas rows de users cadastrado
            users = UserModel.query.all()
            # recebe todas rows de address cadastrado
            adresses = AddressModel.query.all()
            # recebe todas rows the persons cadastrado
            persons = PersonModel.query.all()

            output = []

            for user_row in users:
                for address_row in adresses:
                    for person_row in persons:
                        if user_row.public_id == person_row.user_public_id:
                            person = {}
                            person['cpf_cnpj'] = person_row.cpf_cnpj
                            person['rg'] = person_row.rg
                            person['type_person'] = person_row.type_person.name
                            person['user_public_id'] = person_row.user_public_id
                    if user_row.public_id == address_row.user_public_id:
                        address = {}
                        address['address_public_id'] = address_row.address_public_id
                        address['federal_unity'] = address_row.federal_unity
                        address['postal_code'] = address_row.postal_code
                        address['city'] = address_row.city
                        address['district'] = address_row.district
                        address['street'] = address_row.street
                        address['number'] = address_row.number
                        address['phone'] = address_row.phone
                user_data = {}
                user_data['public_id'] = user_row.public_id
                user_data['name'] = user_row.name
                user_data['person_type'] = person
                user_data['username'] = user_row.username
                user_data['email'] = user_row.email
                user_data['address'] = address
                output.append(user_data)

            current_user = UserModel.query.filter_by(
                public_id=public_id).first()

            if not current_user.admin:
                return make_response(jsonify({'message': 'You are not allow to perform this action.'}),401)

            return make_response(jsonify({'users': output},
                            {'status_code':200}), 200)

        except Exception as ex:
            return make_response(jsonify({'message': f"Something went wrong with the request. Check the parameters and it's values then try again."},
                           {'Exception': f'{ex}'},
                           {'status_code': 500}), 500)


class GetUser(Resource):
    @jwt_required
    def get(self, public_id):

        try:

            session_public_id = get_jwt_identity()

            user = UserModel.query.filter_by(public_id=public_id).first()

            user_address = AddressModel.query.filter_by(
                user_public_id=public_id).first()

            person_row = PersonModel.query.filter_by(
                user_public_id=public_id).first()

            if person_row:
                person = {}
                person['cpf_cnpj'] = person_row.cpf_cnpj
                person['rg'] = person_row.rg
                person['type_person'] = person_row.type_person.name
                person['user_public_id'] = person_row.user_public_id

            if user_address:
                address = {}
                address['address_public_id'] = user_address.address_public_id
                address['federal_unity'] = user_address.federal_unity
                address['postal_code'] = user_address.postal_code
                address['city'] = user_address.city
                address['district'] = user_address.district
                address['street'] = user_address.street
                address['number'] = user_address.number
                address['phone'] = user_address.phone

            if user:
                user_data = {}
                user_data['public_id'] = user.public_id
                user_data['name'] = user.name
                user_data['person_type'] = person
                user_data['username'] = user.username
                user_data['email'] = user.email
                user_data['address'] = address

                return make_response(jsonify({'user': user_data},
                                {'status_code':200}), 200)
            return jsonify({'message': 'No user found with this public id on database.'})
        except Exception as ex:
            return make_response(jsonify({'message': f"Something went wrong with the request. Check the parameters and it's values then try again."},
                           {'Exception': f'{ex}'},
                           {'status_code': 500}), 500)


class UserAccountStatus(Resource):
    @jwt_required
    def put(self):

        try:

            session_public_id = get_jwt_identity()

            current_user = UserModel.query.filter_by(
                public_id=session_public_id).first()

            if current_user.active:
                current_user.active = False
                '''
                TODO: Utilizar esse método também para ativar conta?
                '''
                return make_response(jsonify({'message': f'The user {current_user.name} is now Inactive.'},
                                {'status_code': 200}), 200)

                db.session.close()
                db.session.commit()

        except Exception as ex:
            return make_response(jsonify({'message': f"Something went wrong with the request. Check the parameters and it's values then try again."},
                           {'Exception': f'{ex}'},
                           {'status_code': 500}), 500)
