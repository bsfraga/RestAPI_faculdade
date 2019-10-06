from flask import request, jsonify, make_response
from flask_restful import Resource
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

from controller.user import UserModel

#import app
import datetime

from model.user import UserModel as User

class Login(Resource):
    @classmethod
    def post(self):
        # auth = request.authorization

        # print('\n')
        # print(auth)
        # print('\n')

        # if not auth or not auth.username or not auth.password:
        #     return make_response('Could not verify', 401,
        #                         {'WWW-Authenticate':'Basic realm="Login required."'})
        
        # user = User.query.filter_by(username=auth.username).first()

        # if not user:
        #     return make_response('Could not verify', 401,
        #                         {'WWW-Authenticate':'Basic realm="Login required."'})
        # if check_password_hash(user.password, auth.password):
        #     token = jwt.encode({'public_id': user.public_id,
        #                         'exp':datetime.datetime.utcnow()+datetime.timedelta(60)}, key='DontTellAnyone')
        #     return jsonify({'message':'User successfully logged in.',
        #                     'token':token.decode('UTF-8')})
        # return make_response('Could not verify', 401,
        #                         {'WWW-Authenticate':'Basic realm="Login required."'})

        data = request.get_json()

        user = UserModel.query.filter_by(username=data['username']).first()

        print('\n')
        print(f'Query username: {user}')
        print('\n')

        if user and check_password_hash(user.password, data['password']):
            token = create_access_token(identity=user.public_id)
            return jsonify({
                    'name': user.name,
                    'username': user.username,
                    'email': user.email
                    },{
                    'message':'User logged successfully.'
                    },{'token':token})