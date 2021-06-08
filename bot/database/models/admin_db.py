from sqlalchemy import Column, Integer, String,Date,Text,DateTime
from bot.database import base,session
import datetime
from bot import LOGGER
import threading

LOCK=threading.RLock()


class Admin(base):
    __tablename__='admins'
    id=Column(Integer,primary_key=True)
    chat_id=Column(Integer)

    def __init__(self,chat_id):
        self.chat_id=chat_id  

    def __repr__(self):
        return f'{self.id}'
    
Admin.__table__.create(checkfirst=True)

def get_admin():
    try:
        return [admin.chat_id for admin in session.query(Admin).all()]
    finally :
        session.close()
        
        
def add_admin(chat_id):
    with LOCK:
        session.add(Admin(chat_id=int(chat_id)))
        session.commit()

def total_admins():
    return session.query(Admin).count()
        