from sqlalchemy import Column, Integer, String,Date,Text,DateTime,BigInteger
from sqlalchemy.dialects.postgresql import ARRAY
from bot.database import base,session
import datetime
from bot import LOGGER
import threading

LOCK=threading.RLock()

class Warn(base):
    __tablename__='warn'
    id=Column(Integer,primary_key=True)
    chat_id=Column(BigInteger)
    user_id=Column(Integer)
    no_of_warns=Column(Integer)
    
    def __init__(self,chat_id,user_id,no_of_warns=0):
        self.chat_id=chat_id
        self.user_id=user_id
        self.no_of_warns=no_of_warns
    
    def __repr__(self):
        return self.id

Warn.__table__.create(checkfirst=True)        

class WarnSetting(base):
    __tablename__='warn_settings'
    id=Column(Integer,primary_key=True)
    warns=Column(Integer,default=5)
    mode=Column(String)
    def __init__(self,warns=5,mode='kick'):
        self.warns=warns
        self.mode=mode
    
    def __repr__(self):
        return self.id
    
WarnSetting.__table__.create(checkfirst=True) 


def get_user_warn_count(chat_id : int,user_id : int):
    query=session.query(Warn).filter(Warn.chat_id == chat_id,Warn.user_id==user_id).first()
    return query.no_of_warns

def warn_user(chat_id : int ,user_id: int):
    chat_data = session.query(Warn).filter(Warn.chat_id == chat_id,Warn.user_id==user_id).first()
    with LOCK:
        if not chat_data:
            session.add(Warn(chat_id=chat_id,user_id=user_id,no_of_warns=1))
            session.commit()
            LOGGER.info(f"Initialized Warn Document for {user_id} in {chat_id}")
            
            return 1
        else:
            session.query(Warn).filter(
                Warn.chat_id == chat_id,Warn.user_id==user_id).update({
                                                                Warn.no_of_warns : Warn.no_of_warns+1 })
            session.commit()
            
            return chat_data.no_of_warns

def remove_warn(chat_id : int ,user_id : int):
    try:
        with LOCK:
            session.query(Warn).filter(
                        Warn.chat_id == chat_id,Warn.user_id==user_id).update({
                                                                        Warn.no_of_warns : Warn.no_of_warns - 1 })
            session.commit()
    finally:
        session.close()
        
def reset_warn(chat_id : int ,user_id : int):
    with LOCK:
            session.query(Warn).filter(
                        Warn.chat_id == chat_id,Warn.user_id==user_id).delete()
            session.commit()
            
def total_warns():
    warns=session.query(Warn).all()
    return sum(warn.no_of_warns for warn in warns)

def total_warned_user():
    users=session.query(Warn).count()
    return users

def set_warn_limit(limit : int):
    with LOCK:
        settings=session.query(WarnSetting).first()
        if not settings:
            session.add(WarnSetting(warns=limit))
            session.commit()
        else:
            session.query(WarnSetting).filter(WarnSetting.id==1).update({WarnSetting.warns: limit})
            session.commit()
            
def set_warn_mode(mode : str ):
    with LOCK:
        settings=session.query(WarnSetting).first()
        if not settings:
            session.add(WarnSetting(mode=mode.lower()))
            session.commit()
        else:
            session.query(WarnSetting).filter(WarnSetting.id==1).update({WarnSetting.mode: mode.lower()})
            session.commit()

def get_warn_settings():
    query=session.query(WarnSetting).first()
    return query.warns,query.mode