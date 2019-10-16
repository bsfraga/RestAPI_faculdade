import uuid
from functools import wraps

import jwt
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from controller.sql_alchemy import db
from model.address import AddressModel
from model.user import UserModel
from model.person import PersonModel

'''
TODO: adicionar métodos get
    - exibir valores de person_model
'''


class NewUser(Resource):
    def post(self):
        data = request.get_json()

        hashed_password = generate_password_hash(
            data['password'], method='sha256')

        new_user = UserModel(public_id=str(uuid.uuid4()),
                             name=data['name'],
                             username=data['username'],
                             email=data['email'],
                             password=hashed_password,
                             admin=False)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User successfully created.'},
                       {new_user.json()},
                       {'status code: 201'})


class GetUsers(Resource):
    @jwt_required
    def get(self):
        '''
        TODO: atualizar método get
        '''

        public_id = get_jwt_identity()

        '''
        TODO: Decidir scopo de visão de todos users
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

        current_user = UserModel.query.filter_by(public_id=public_id).first()

        if not current_user.admin:
            return jsonify({'message': 'You are not allow to perform this action.'})

        return jsonify({'users': output})


class GetUser(Resource):
    @jwt_required
    def get(self, public_id):
        '''
        TODO: atualizar método get
        '''

        session_public_id = get_jwt_identity()

        '''
        current_user = UserModel.query.filter_by(public_id=session_public_id).first()
        Não sei se deixo essa validao >.<
        '''
        # if not current_user.admin:
        #     return jsonify({'message':'You are not allow to perform this action.'})

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

            return jsonify({'user': user_data})
        return jsonify({'message': 'No user found with this public id on database.'})


class PromoteUser(Resource):
    @jwt_required
    def put(self, public_id):

        session_public_id = get_jwt_identity()

        current_user = UserModel.query.filter_by(
            public_id=session_public_id).first()

        '''-> Este trecho mantém comentado enquanto estiver em DESENVOLVIMENTO
        if not current_user.admin:
            return jsonify({'message':'You are not allow to perform this action.'})'''

        db.session.close()

        user = UserModel.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message': 'No user found with this public id on database.'})

        user.admin = True
        db.session.commit()

        return jsonify({'message': f'The user {user.name} has been promoted to Admin.'}, 201)


class DeleteUser(Resource):
    @jwt_required
    def delete(self, public_id):

        session_public_id = get_jwt_identity()

        current_user = UserModel.query.filter_by(
            public_id=session_public_id).first()

        if not current_user.admin:
            return jsonify({'message': 'You are not allowed to perform this action.'})
        db.session.close()

        user = UserModel.query.filter_by(public_id=public_id).first()

        user_address = AddressModel.query.filter_by(user_id=user.id).first()
        if not user:
            return jsonify({'message': 'No user found with this "public_id" on database.'})

        db.session.delete(user_address)
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'An user has just been deleted from the database successfully.'})
