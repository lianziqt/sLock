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
    COMMOM = 1
    DORLEADER = 2
    MANAGER = 4
    ADMIN = 8

class Dormitory(db.model):
    __tablename__='dormitory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    password_hash = db.Column(db.String(128))
    building_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    students = db.relationship('Student', backref='dor', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Dormitory, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        dormitory = Dormitory.query.get(data.get('reset'))
        if dormitory is None:
            return False
        dormitory.password = new_password
        db.session.add(dormitory)
        return True


class Manager(db.model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    work_num = db.Column(db.String(16))
    name = db.Column(db.String(10))
    password_hash = db.Column(db.String(128))
    apartment_name = db.Column(db.Integer)
    dormitories = db.relationship('Dormitory', backref='manager')
    #外键

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        manager = Manager.query.get(data.get('reset'))
        if manager is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True
        
class Student(db.model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String(16))
    name = db.Column(db.String(10))
    sex = db.Column(db.Integer)
    door_id = db.Column(db.Integer, db.ForeignKey('dormitory.id'))
    start_year = db.Column(db.Integer)
    def __init__(self, **kwargs):
        super(Student, self).__init__(**kwargs)


class Record(db.model):
    __tablename__ = 'records'
    door_id = db.Column(db.Integer, db.ForeignKey('dormitory.id'), primary_key=True)###########
    time = db.Column(db.DateTime(), default=datetime.utcnow, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))##########
    unlock_way = db.Column(db.Integer)
    result = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        super(Record, self).__init__(**kwargs)
        

class Key(db.model):
    __tablename__ = 'keys'
    student_id = db.Column(db.Integer)###########
    IC_card = db.Column(db.String(255), unique=True)
    status = db.Column(db.Integer)
    fingerprint = db.Column(db.String(255), unique=True)
    voice = db.Column(db.String(255), unique=True)
    face = db.Column(db.String(255), unique=True)

    def __init__(self, **kwargs):
        super(Key, self).__init__(**kwargs)

class Message(db.model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)###########
    dormitory_id = db.Column(db.Integer, db.ForeignKey('dormitory.id'))
    typee = db.Column(db.Integer)
    time = db.Column(db.DateTime(), index=True,  default=datetime.utcnow)
    details = db.Column(db.Text())

    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)
        
        