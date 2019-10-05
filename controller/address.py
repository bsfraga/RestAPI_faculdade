import uuid
import jwt
from functools import wraps

from flask import jsonify, request
from flask_restful import Resource
from model.address import AddressModel
from model.user import UserModel
from controller.sql_alchemy import db

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        print("\n")
        print("Request Headers Data:\n")
        print(request.headers)
        print("\n")

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing.'})
        
        try:
            data = jwt.decode(token, key='DontTellAnyone')
            current_user = UserModel.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


class NewAddress(Resource):
    def post(self, public_id):
        data = request.get_json()

        if public_id == None:
            return jsonify({'message': 'You must inform a "public_id" so the address can be linked to the user.'}, 400)

        user_data = UserModel.query.filter_by(public_id=public_id).first()

        new_address = AddressModel(public_id=str(uuid.uuid4()),
                                    federal_unity=data['federal_unity'],
                                    postal_code=data['postal_code'],
                                    city=data['city'],
                                    district=data['district'],
                                    street=data['street'],
                                    number=data['number'],
                                    phone=data['phone'],
                                    user_id=user_data.id)
        
        db.session.add(new_address)
        db.session.commit()

        return jsonify({'message':'Successfully registred an Address.'},
                        {
                        'public_id': new_address.public_id,
                        'federal_unity': new_address.federal_unity,
                        'postal_code': new_address.postal_code,
                        'city': new_address.city,
                        'district': new_address.district,
                        'street': new_address.street,
                        'number': new_address.number,
                        'phone': new_address.phone,
                        }, 201)

class UpdateAddress(Resource):
    @token_required
    def put(current_user, self, public_id):

        data = request.get_json()
        address = AddressModel.query.filter_by(current_user=current_user.public_id).first()

        if not address:
            return jsonify({'message':"You must inform the address['public_id']"}, 404)

        user_data = UserModel.query.filter_by(public_id=current_user).first()

        new_address = AddressModel(public_id=str(uuid.uuid4()),
                                    federal_unity=data['federal_unity'],
                                    postal_code=data['postal_code'],
                                    city=data['city'],
                                    district=data['district'],
                                    street=data['street'],
                                    number=data['number'],
                                    phone=data['phone'],
                                    user_id=user_data.id)

        address += new_address
        db.session.commit()

        return jsonify({'message':'Address updated successfully..'},
                        {
                        'public_id': new_address.public_id,
                        'federal_unity': new_address.federal_unity,
                        'postal_code': new_address.postal_code,
                        'city': new_address.city,
                        'district': new_address.district,
                        'street': new_address.street,
                        'number': new_address.number,
                        'phone': new_address.phone,
                        }, 201)
#TODO: verificar pq este método nao tem acesso ao current_user com o public_id