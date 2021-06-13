from sqlalchemy import Column, Integer, String,Date,Text,DateTime,BigInteger
from bot.database import base,session
import datetime
from bot import LOGGER
import threading

LOCK=threading.RLock()


class Admin(base):
    __tablename__='admins'
    id=Column(Integer,primary_key=True)
    chat_id=Column(Integer)
    username=Column(String)
    name=Column(String)
    date=Column(DateTime,default=datetime.datetime.now())

    def __init__(self,chat_id,username,name):
        self.chat_id=chat_id  
        self.username=username
        self.name=name

    def __repr__(self):
        return f'{self.id}'
    
Admin.__table__.create(checkfirst=True)

class Group(base):
    __tablename__='groups'
    id=Column(Integer,primary_key=True)
    group_id=Column(BigInteger)
    group_name=Column(String)
    username=Column(String)
    added_by=Column(Integer)
    
    def __init__(self,group_id,group_name,username,added_by):
        self.group_id=group_id 
        self.username=username
        self.group_name=group_name
        self.added_by=added_by

    def __repr__(self):
        return f'{self.id}'
    
Group.__table__.create(checkfirst=True)

def add_group(id,username,name,added_by):
    with LOCK:
        session.add(Group(group_id=id,group_name=name,username=username,added_by=added_by))
        session.commit()
        
def remove_group(id):
    with LOCK:
        session.query(Group).filter(Group.group_id==id).delete()
        session.commit()

def get_group():
    try:
        total_group=session.query(Group).count()
        data=""
        for group in session.query(Group).all():
            data+=f'ID : {group.group_id}\nName : {group.group_name}\nUsername : {group.username}\nAdded by : {group.added_by}\n\n'
        return f"Total Groups : {total_group}\n\n {data}"
    finally :
        session.close()

def get_group_id():
    return[i.group_id for i in session.query(Group)]
        
def get_admin():
    
        return [admin.chat_id for admin in session.query(Admin)]
        
        
def add_admin(chat_id,username,name):
    with LOCK:
        session.add(Admin(chat_id=int(chat_id),username=username,name=name))
        session.commit()

def total_admins():
    return session.query(Admin).count()

def get_admin_info():
    data=""
    for admin in session.query(Admin):
        data+=f" ID : {admin.chat_id}\nUsername : {admin.username}\nName : {admin.name}\n Date : {admin.date}\n\n"
    return data
        
def remove_admin(chat_id):
    with LOCK:
        session.query(Admin).filter(Admin.chat_id==chat_id).delete()
        session.commit()
        
        