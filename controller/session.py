import datetime

from flask import jsonify, make_response, request
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required
from flask_restful import Resource
from werkzeug.security import check_password_hash

from controller.blacklist import BLACKLIST
from controller.user import UserModel
from model.user import UserModel as User


class Login(Resource):
    @classmethod
    def post(self):

        data = request.get_json()

        if not data or not data['username'] or not data['password']:
            return make_response('Could not verify', 401,
                                 {'WWW-Authenticate': 'Basic realm="Login required."'})

        user = UserModel.query.filter_by(username=data['username']).first()

        if not user:
            return make_response('Could not verify', 401,
                                 {'WWW-Authenticate': 'Basic realm="Login required."'})

        if check_password_hash(user.password, data['password']):
            token = create_access_token(identity=user.public_id)
            return jsonify({'public_id': user.public_id,
                            'name': user.name,
                            'username': user.username,
                            'email': user.email},
                            {'message': 'User logged successfully.'},
                            {'token': token},
                            {'status_code': 200})

        return make_response('Could not verify', 401,
                             {'WWW-Authenticate': 'Basic realm="Login required."'})


class Logout(Resource):
    @jwt_required
    def post(cls):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return jsonify({'message': 'User has been successfully desconected.'},
                       {'status_code': 200})
