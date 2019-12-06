from controller.sql_alchemy import db
from model.conversation import ConversationModel

class ConversationReplyModel(db.Model):
    __tablename__ = 'conversation_reply'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    
    #Foreing Keys (one to many)
    conversation_public_id = db.Column(db.String(80), db.ForeignKey('conversation.conversation_public_id'), nullable=False)
    user_public_id = db.Column(db.String(80), db.ForeingKey('user.user_public_id'), nullable=False)

    reply_public_id = db.Column(db.Integer, unique=True, nullable=False)
    message = db.Column(db.Text)
    time = db.Column(db.DateTime)



