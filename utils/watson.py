import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

'''
Basic authentication
Context variables

TODO 1: Ajustar Excepts
TODO 2: Ajustar retornos
TODO 3: Validar se funciona
TODO 4: Criar classe de log no Banco para requisições de dialogo
TODO 5: Criar endpoints

'''

apikey = 'MECtWP_A-UvB97BSSqQkxBVW3QFtTqfl2tDmiSaNimGH'
url = 'https://gateway.watsonplatform.net/assistant/api'
version = '2019-02-28'
assistant_id = 'a7b32be5-3e7e-4947-bf0f-98f976b7da38'

#############################################################

authenticator = IAMAuthenticator(apikey)
service = AssistantV2(version=version,
                        authenticator=authenticator)

service.set_service_url(url)


class WatsonCore():

    def create_session(self):
        '''
        This method initialize the session from Watson Assistant and get the first dialog message from it.
        If request is OK, return session_id as JSON Object.
        Else return None
        '''    
        try:

            session_id = service.create_session(assistant_id=assistant_id).get_result()

            return session_id

        except Exception as ex:
            print(f'Exception: {ex}')
            return None


    def dialog_message(self, message:str=None):
        '''
        This method makes the dialog request with Watson Assistant.
        If request is OK, return message.
        Else return None
        '''
        try:
            session_id = create_session()

            if message:
                message_response = service.message(assistant_id=assistant_id,
                                                    session_id=session_id['session_id'],
                                                    input={'message_type':'text',
                                                            'text':f'{message}'}).get_result()
            else:                                                            
                message_response = service.message(assistant_id=assistant_id,
                                                    session_id=session_id['session_id'],
                                                    input={'message_type':'text',
                                                            'text':''}).get_result()

            for r in message_response['output']['generic']:
                message = r['text']

            return message

        except Exception as ex:
            print(f'Exception: {ex}')
            return None

    def end_session(self):
        '''
        This method ends the dialog session with the Watson Assistant.
        If request OK, return JSON response
        Else, Return None
        '''
        try:
            
            session_id = create_session()

            close_session = service.delete_session(assistant_id=assistant_id,
                                                    session_id=session_id['session_id']).get_result()

            return close_session
        
        except Exception as ex:
            print(f'Exception: {ex}')
            return None