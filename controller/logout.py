from flask_jwt_extended import get_raw_jwt, jwt_required
from flask_restful import Resource
from controller.blacklist import BLACKLIST


class Logout(Resource):
    @jwt_required
    def post(cls):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message':'User has been successfully desconected.'}
