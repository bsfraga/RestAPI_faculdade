from controller.sql_alchemy import db
from model.user import UserModel

class ConversationModel(db.Model):
    __tablename__ = 'conversation'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    conversation_public_id = db.Column(db.String(80), nullable=False, unique=True)
    watson_session_id = db.Column(db.String(80), nullable=False, unique=True)
    status = db.Column(db.Integer, nullable=False)
    
    #   one to many relationship
    user_public_id = db.relationship(UserModel, backref='address', lazy=True)