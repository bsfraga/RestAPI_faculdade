from flask import request, jsonify, make_response
from flask_restful import Resource
from werkzeug.security import check_password_hash

#import app
import jwt
import datetime

from model.user import UserModel as User

class Login(Resource):
    def post(self):
        auth = request.authorization

        print('\n')
        print(auth)
        print('\n')

        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401,
                                {'WWW-Authenticate':'Basic realm="Login required."'})
        
        user = User.query.filter_by(username=auth.username).first()

        if not user:
            return make_response('Could not verify', 401,
                                {'WWW-Authenticate':'Basic realm="Login required."'})
        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': user.public_id,
                                'exp':datetime.datetime.utcnow()+datetime.timedelta(60)}, key='DontTellAnyone')
            return jsonify({'message':'User successfully logged in.',
                            'token':token.decode('UTF-8')})
        return make_response('Could not verify', 401,
                                {'WWW-Authenticate':'Basic realm="Login required."'})

