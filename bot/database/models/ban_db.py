from sqlalchemy import Column, Integer, String,Date,Text,DateTime,BigInteger
from bot.database import base,session
import datetime
from bot import LOGGER
import threading

LOCK=threading.RLock()

class BannedUser(base):
    __tablename__='banned_users'
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer)
    name=Column(String)
    
    def __init__(self,user_id,name):
        self.user_id=user_id
        self.name=name
        
    def __repr__(self):
        return f"{self.user_id}"
    
BannedUser.__table__.create(checkfirst=True)

class Spam(base):
    __tablename__='spam'
    id=Column(Integer,primary_key=True)
    text=Column(String)
    
    def __init__(self,text):
        self.text=text
        
    def __repr__(self):
        return f"{self.id}"
    
Spam.__table__.create(checkfirst=True)

def add_spam(text):
    with LOCK:
        session.add(Spam(text=text))
        session.commit()

def get_spam_text():
    try:
        return [text.text for text in session.query(Spam)]
    finally:
        session.close()

def add_ban_user(user_id,name):
    with LOCK:
        session.add(BannedUser(user_id=user_id,name=name))
        session.commit()

def get_ban_user_data():
    
    count=session.query(BannedUser).count()
    data=[user for user in session.query(BannedUser) ]
    return count,data

def get_ban_user(user_id):
    return session.query(BannedUser).filter(BannedUser.user_id==user_id).first()

def remove_ban(user_id):
    with LOCK:
        session.query(BannedUser).filter(BannedUser.user_id==user_id).delete()
        session.commit()