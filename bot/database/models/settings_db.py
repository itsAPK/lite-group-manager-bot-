from sqlalchemy import Column, Integer, String,Date,Text,DateTime
from bot.database import base,session
import datetime
from bot import LOGGER
import threading

LOCK=threading.RLock()


class Welcome(base):
    __tablename__='welcome'
    id=Column(Integer,primary_key=True)
    text=Column(String)

    def __init__(self,text):
        self.text=text

    def __repr__(self):
        return f'{self.id}'
    
Welcome.__table__.create(checkfirst=True)

class Button(base):
    __tablename__='button'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    url=Column(String)
    
    def __init__(self,name,url):
        self.name=name
        self.url=url
        
    def __repr__(self):
        return self.id
    
Button.__table__.create(checkfirst=True)

class Task(base):
    __tablename__='task'
    id=Column(Integer,primary_key=True)
    task_id=Column(String)
    text=Column(String)
    

    def __init__(self,task_id,text):
        self.task_id=task_id
        self.text=text

    def __repr__(self):
        return f'{self.id}'

Task.__table__.create(checkfirst=True)




def set_welcome_message(text):
    col=session.query(Welcome).first()
    if not col:
        session.add(Welcome(text=text))
        session.commit()
    else:
        session.query(Welcome).filter(Welcome.id==1).update({Welcome.text : text})
        session.commit()
    
def get_welcome_message():
    col=session.query(Welcome).first()
    return col

def add_button(name,url):
    
    session.add(Button(name=name,url=url))
    session.commit()
    
def get_buttons():
        return  session.query(Button).all()
    
def delete_button(id):
    session.query(Button).filter(Button.id==id).delete()
    session.commit()
    
def add_task(task_id,text):
    with LOCK:
        session.add(Task(task_id=task_id,text=text))
        session.commit()
    
def get_task_data(task_id):
    try:
        query=session.query(Task).filter(Task.task_id==task_id).first()
        return query
    finally:
        session.close()
        
def delete_task(task_id):
    with LOCK:
        session.query(Task).filter(Task.task_id==task_id).delete()
        session.commit()
        
        
def delete_all_task():
    with LOCK:
        session.query(Task).delete()
        session.commit()