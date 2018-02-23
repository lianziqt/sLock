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

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    dormitory = db.relationship('Dormitory', backref='role', lazy='dynamic')
    manager = db.relationship('Manager', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'Dromitory': [Permission.COMMOM, Permission.DORLEADER],
            'Administrator': [Permission.COMMOM, Permission.DORLEADER,
                              Permission.ADMIN],
        }
        default_role = 'Dormitory'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name

class Dormitory(db.model):
    __tablename__='dormitory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), unique=True)
    password_hash = db.Column(db.String(128))
    lock_online = db.Column(db.Boolean)
    student_num = db.Column(db.Integer)
    manager_id = db.Column(db.Integer, db.ForeignKey('managers.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
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

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

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

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class Manager(db.model):
    __tablename__ = 'managers'
    id = db.Column(db.Integer, primary_key=True)
    work_num = db.Column(db.String(16))
    name = db.Column(db.String(10))
    password_hash = db.Column(db.String(128))
    apartment_name = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    dormitories = db.relationship('Dormitory', backref='manager')
    #外键

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def verify_password(self, password):
            return check_password_hash(self.password_hash, password)


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

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
        
class Student(db.model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    studentid = db.Column(db.String(16))
    name = db.Column(db.String(10))
    sex = db.Column(db.Integer)
    dormitory_id = db.Column(db.Integer, db.ForeignKey('dormitory.id'))
    start_year = db.Column(db.Integer)
    def __init__(self, **kwargs):
        super(Student, self).__init__(**kwargs)

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class Record(db.model):
    __tablename__ = 'records'
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), primary_key=True)
    dormitory_id = db.Column(db.Integer, db.ForeignKey('dormitory.id'), primary_key=True)###########
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
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    typee = db.Column(db.Integer)
    time = db.Column(db.DateTime(), index=True,  default=datetime.utcnow)
    details = db.Column(db.Text())
    complete = db.Column(db.Boolean(),default=False)

    def __init__(self, **kwargs):
        super(Message, self).__init__(**kwargs)
        
        