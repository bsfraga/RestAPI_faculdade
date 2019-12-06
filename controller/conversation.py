import uuid

from flask import jsonify, request, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource

from controller.sql_alchemy import db
from utils.watson import WatsonCore
from model.user import UserModel
from model.address import AddressModel

#TODO: criar classe de validação de dados informados pelo usuario para ser utilizado nessa classe e na classe USER(Request)

class NewRegister(Resource):
    '''
    This class is responsable to make the conversation and create a new user into the system.

    Required information:
        User
            Name, Username, Email, Password
        Address
            federal_unity, postal_code, city, district, street, number, phone

    '''
    def post(self):

        '''
        receber os parametros nessa request e passar os valores, após validados, para o request de user
        '''

        try:
            
            session_id = WatsonCore.create_session()

            if not session_id:
                return make_response(jsonify({'message': "Wasn't possivel to create a new session. Please, contact the devs."}, {'status_code':500}), 500)
            
            data = request.get_json()

            msg_response = WatsonCore.dialog_message(data)

            return msg_response

        except Exception as e:
            return make_response(jsonify({'message':'An internal error has ocurred.'}, {'Exception': f'{e}'}, {'status_code':500}), 500)



class NewConversation(Resouce):
    @jwt_required
    def post(self):

        try:

            '''
            Recuperar os dados do user para salvar no objeto ConversationModel

            Watson
                Criar Sessão
                Enviar Mensagem

            *Verificar quando encerrar sessão
            '''

        except Exception as e:
            return make_response(jsonify({'message':'An internal error has ocurred.'}, {'Exception': f'{e}'}, {'status_code':500}), 500)