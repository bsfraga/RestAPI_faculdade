import uuid
import jwt
from functools import wraps

from flask import jsonify, request
from flask_restful import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from controller.sql_alchemy import db
from model.user import UserModel
from model.address import AddressModel


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


class NewUser(Resource):
    def post(self):
        data = request.get_json()
        print("\n")
        print("Login Data:\n")
        print(data)
        print("\n")

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = UserModel(public_id=str(uuid.uuid4()),
                        name=data['name'],
                        username=data['username'],
                        email=data['email'],
                        password=hashed_password,
                        admin=False)
                        

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User successfully created.'},
                        {
                        'public_id': new_user.public_id,
                        'name': new_user.name,
                        'username': new_user.username,
                        'email': new_user.email,
                        'admin': new_user.admin
                        })



class GetUsers(Resource):
    @token_required
    def get(current_user, self):

        if not current_user.admin:
            return jsonify({'message':'You are not allow to perform this action.'})

        users = UserModel.query.all()

        output = []

        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['username'] = user.username
            user_data['email'] = user.email
            user_data['address'] = user.address
            
            output.append(user_data)

        return jsonify({'users': output})


class GetUser(Resource):
    @token_required
    def get(current_user, self, public_id):

        if not current_user.admin:
            return jsonify({'message':'You are not allow to perform this action.'})

        user = UserModel.query.filter_by(public_id=public_id).first()

        user_address = AddressModel.query.filter_by(user_id=user.id).first()
        
        if user_address:
            address = {}
            address['public_id'] = user_address.public_id
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
            user_data['username'] = user.username
            user_data['email'] = user.email
            user_data['address'] = address


            return jsonify({'user':user_data})
        return jsonify({'message':'No user found with this public id on database.'})



class PromoteUser(Resource):
    @token_required
    def put(current_user, public_id, self):

        if not current_user.admin:
            return jsonify({'message':'You are not allow to perform this action.'})

        user = UserModel.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message':'No user found with this public id on database.'})

        user.admin = True
        db.session.commit()

        return jsonify({'message': f'The user {user.name} has been promoted to Admin.'}, 404)


class DeleteUser(Resource):
    @token_required
    def delete(current_user, self, public_id):

        if not current_user.admin:
            return jsonify({'message':'You are not allow to perform this action.'})

        user = UserModel.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message':'No user found with this public id on database.'})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message':'An user has just been deleted from the database successfully.'})
