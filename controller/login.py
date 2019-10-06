import datetime

from flask import jsonify, make_response, request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from werkzeug.security import check_password_hash

from controller.user import UserModel
from model.user import UserModel as User


class Login(Resource):
    @classmethod
    def post(self):

        data = request.get_json()
        
        if not data or not data['username'] or not data['password']:
            return make_response('Could not verify', 401,
                                {'WWW-Authenticate':'Basic realm="Login required."'})


        user = UserModel.query.filter_by(username=data['username']).first()

        if not user:
            return make_response('Could not verify', 401,
                                {'WWW-Authenticate':'Basic realm="Login required."'})

        if check_password_hash(user.password, data['password']):
            token = create_access_token(identity=user.public_id)
            return jsonify({
                    'name': user.name,
                    'username': user.username,
                    'email': user.email
                    },{
                    'message':'User logged successfully.'
                    },{'token':token})
        
        return make_response('Could not verify', 401,
                                {'WWW-Authenticate':'Basic realm="Login required."'})
