from flask import Flask, jsonify, request
#from flask_jwt_extended import JWTManager
from flask_restful import Api
import jwt

from controller.user import NewUser, GetUsers, GetUser, PromoteUser, DeleteUser
from controller.address import NewAddress, UpdateAddress
from controller.login import Login


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:25885c@192.168.0.6:3306/api_faculdade_v2'
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config['JWT_BLACKLIST_ENABLED'] = True

@app.before_first_request
def cria_banco():
    db.create_all()

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