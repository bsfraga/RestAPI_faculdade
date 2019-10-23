import uuid
from functools import wraps

import jwt
from flask import jsonify, request, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from controller.sql_alchemy import db
from model.address import AddressModel
from model.user import UserModel


class NewAddress(Resource):
    def post(self, public_id):

        try:

            data = request.get_json()

            if public_id == None:
                return make_response(jsonify({'message': 'You must inform a "public_id" so the address can be linked to the user.'}, {'stats_code': 400}), 400)

            new_address = AddressModel(address_public_id=str(uuid.uuid4()),
                                       federal_unity=data['federal_unity'],
                                       postal_code=data['postal_code'],
                                       city=data['city'],
                                       district=data['district'],
                                       street=data['street'],
                                       number=data['number'],
                                       phone=data['phone'],
                                       user_public_id=public_id)

            db.session.add(new_address)
            db.session.commit()

            return make_response(jsonify({'message': 'Successfully registred an Address to an User.'}, {'address': new_address.json()}, {'status code': 201}), 201)
        
        except Exception as ex:
            return make_response(jsonify({'message': f"Something went wrong with the request. Check the parameters and it's values then try again."},
                           {'Exception': f'{ex}'},
                           {'status_code': 500}), 500)


class UpdateAddress(Resource):
    @jwt_required
    def put(self, address_public_id):

        try:

            data = request.get_json()
            public_id = get_jwt_identity()

            address = AddressModel.query.filter_by(
                address_public_id=address_public_id).first()

            if not address:
                return make_response(jsonify({'message': "You must inform the address['public_id']"}, {'status_code': 404}), 404)

            user_data = UserModel.query.filter_by(public_id=public_id).first()

            new_address = AddressModel(address_public_id=str(uuid.uuid4()),
                                       federal_unity=data['federal_unity'],
                                       postal_code=data['postal_code'],
                                       city=data['city'],
                                       district=data['district'],
                                       street=data['street'],
                                       number=data['number'],
                                       phone=data['phone'],
                                       user_id=user_data.id)
            AddressModel.query.filter_by(address_public_id=address_public_id).update({
                'address_public_id': new_address.address_public_id,
                'federal_unity': new_address.federal_unity,
                'postal_code': new_address.postal_code,
                'city': new_address.city,
                'district': new_address.district,
                'street': new_address.street,
                'number': new_address.number,
                'phone': new_address.phone
            })
            db.session.commit()

            return make_response(jsonify({'message': 'Address updated successfully..'},
                           {
                'public_id': new_address.address_public_id,
                'federal_unity': new_address.federal_unity,
                'postal_code': new_address.postal_code,
                'city': new_address.city,
                'district': new_address.district,
                'street': new_address.street,
                'number': new_address.number,
                'phone': new_address.phone,
            }, {'status_code':201}), 201)
            
        except Exception as ex:
            return make_response(jsonify({'message': f"Something went wrong with the request. Check the parameters and it's values then try again."},
                           {'Exception': f'{ex}'},
                           {'status_code': 500}), 500)
