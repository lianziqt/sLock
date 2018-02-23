from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,DateField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField
from ..models import Message

class MseeageForm(FlaskForm):
    details = PageDownField("What's on your mind?", validators=[DataRequired()])
    typee = SelectField("信息类别", validators=[DataRequired()], choices=[('1','水'),('2','电'),('3','气'),('4','其它类'),('5','非维修申请')])
    submit = SubmitField('Submit')

class RecordSearchForm(FLaskForm):
    dor_name = StringField("宿舍名")
    #student = StringField("学生学号")
    time = DateField('开锁日期')
    submit = SubmitField("提交")

class DormitorySearchForm(FlaskForm):
    student_num = SelectField("宿舍人数",choices=[('1','1'),('2','2'),('3','3'),('4','4')])
    lock_online = BooleanField("门锁状态")
    submit = SubmitField("提交")

class StudentSearchForm(FlaskForm):
    id = StringField("学号")
    name = StringField("姓名")
    dor_name = StringField("宿舍")
    year = StringField("入学年份")
    submit = SubmitField("提交")
    
class MessageSearchForm(FlaskForm):
    dor_name = StringField("宿舍")
    typee = SelectField("信息类别", validators=[DataRequired()], choices=[('1','水'),('2','电'),('3','气'),('4','其它类'),('5','非维修申请')])
    submit = SubmitField(提交)