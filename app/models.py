from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from markdown import markdown
import bleach
from flask import current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Dormitory(db.model):
    __tablename__='dormitory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    password_hash = db.Column(db.String(128))
    bed_num = db.Column(db.Integer)
    def __init__(self, *args):
        super(Dormitory, self).__init__(*args))

class Manager(db.model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    work_num = db.Column(db.String(16))
    name = db.Column(db.String(10))
    password_hash = db.Column(db.String(128))
    apartment_name = db.Column(db.Integer)
    #外键

    def __init__(self, *args):
        super(Manager, self).__init__(*args))
        
class Student(db.model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String(16))
    name = db.Column(db.String(10))
    sex = db.Column(db.Integer)
    door_id = db.Column(db.Integer)#######
    start_year = db.Column(db.Integer)
    def __init__(self, *args):
        super(Student,db.model.__init__(*args))


class Record(db.model):
    __tablename__ = 'records'
    door_id = db.Column(db.Integer)###########
    time = db.Column(db.DateTime(), default=datetime.utcnow)
    student_id = db.Column(db.Integer)##########
    unlock_way = db.Column(db.Integer)
    result = db.Column(db.Boolean)
    def __init__(self, *args):
        super(Record,db.model.__init__(*args))
        

class Key(db.model):
    __tablename__ = 'keys'
    student_id = db.Column(db.Integer)###########
    IC_card = db.Column(db.String(255), unique=True)
    status = db.Column(db.Integer)
    fingerprint = db.Column(db.String(255), unique=True)
    voice = db.Column(db.String(255), unique=True)
    face = db.Column(db.String(255), unique=True)
    def __init__(self, *args):
        super(Key,db.model.__init__(*args))

class Message(db.model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)###########
    student_id = db.Column(db.Integer)
    sort = db.Column(db.Integer)
    time = db.Column(db.DateTime(), default=datetime.utcnow)
    details = db.Column(db.Text())

    def __init__(self, *args):
        super(Message,db.model.__init__(*args))
        
        