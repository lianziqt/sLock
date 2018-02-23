from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from . import main
from .forms import MessageSearchForm,StudentSearchForm,DormitorySearchForm,RecordSearchForm,MseeageForm
from .. import db
from ..models import Dormitory,Manager,Student,Message,Record,Permission
from ..decorators import admin_required, permission_required'

@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('.record'))
    else:
        return redirect(url_for('auth.login'))

@main.route('/reocrd', methods=['GET', 'POST'])
@login_required
def record():\
    form = RecordSearchForm()
    if current_user.can(Permission.ADMIN):
        query = Record.query.join(Dormitory, Record.dormitory_id == Dormitory.id).filter(Record.manager_id==current_user.id)
        if form.validate_on_submit():
            if form.dor_name.data is not None:
                query = query.filter(Dormitory.name == form.dor_name.data)
            if form.time.data is not None:
                query = query.filter(Record.time == form.time.data)
        pagination = query.order_by(Record.time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        records = pagination.items
    else:
        query = Record.query.filter(Record.dormitory_id == current_user.id)
        if form.validate_on_submit():
            if form.time.data is not None:
                query = query.filter(Record.time == form.time.data)
        pagination = query.order_by(Record.time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        records = pagination.items
    return render_template('record.html',form=form, records=records, pagination=pagination)


@main.route('/message',methods=['GET', 'POST'])   
@login_required
def message():
    form = MessageSearchForm()
    if current_user.can(Permission.ADMIN):
        query = Message.query.join(Dormitory, Message.dormitory_id == Dormitory.id).filter(Message.manager_id==current_user.id)
        if form.validate_on_submit():
            if form.dor_name.data is not None:
                query = query.filter(Dormitory.name == form.dor_name.data)
            if form.typee.data is not None:
                query = query.filter(Message.typee == form.typee.data)
        pagination = query.order_by(Message.time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        messages = pagination.items
    else:
        query = Message.query.filter_by(dormitory_id=current_user.id)
        pagination = query.order_by(Message.time.desc()).paginate(
            page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
            error_out=False)
        messages = pagination.items
    return render_template('message.html',form=form, messages=messages, pagination=pagination)

@main.route('/post-message',methods=['GET', 'POST'])  
@login_required
def post_message():
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(dormitory_id=current_user.id, 
                        manager_id=current_user.manager_id,
                        typee=form.typee.data,
                        details=form.details.data)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for('.message'))
    return render_template('post_message.hrml', form=form)
        
