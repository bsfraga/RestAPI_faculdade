from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_restful import Api

from controller.address import NewAddress, UpdateAddress
from controller.blacklist import BLACKLIST
from controller.login import Login
from controller.user import DeleteUser, GetUser, GetUsers, NewUser, PromoteUser

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:25885c@192.168.0.6:3306/api_faculdade_v2'
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

@app.before_first_request
def cria_banco():
    db.create_all()
#--------------------------JWT Configuration------------------#
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def verify_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def invalid_token():
    return jsonify({'message':'You are not logged in.'}), 401
#-------------------------------------------------------------#

#--------------------------Endpoints--------------------------#
api = Api(app)

#--------------------------Login/Logout-----------------------#
api.add_resource(Login, '/signin')

#--------------------------User-------------------------------#
api.add_resource(NewUser, '/signup')
api.add_resource(NewAddress, '/signup_address/<public_id>')
api.add_resource(UpdateAddress, '/update_address/<public_id>')
api.add_resource(GetUsers, '/users')
api.add_resource(GetUser, '/user/<public_id>')
api.add_resource(PromoteUser, '/user/<public_id>')
api.add_resource(DeleteUser, '/user/<public_id>')
#-------------------------------------------------------------#

if __name__ == '__main__':
    from controller.sql_alchemy import db
    db.init_app(app)
    app.run(debug=True)
