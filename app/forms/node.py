import re
from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, ValidationError, Regexp


class Node(FlaskForm):
    _id = StringField('_id', validators=[Regexp(r'^[\d\w]{24,26}$', re.RegexFlag.I, 'id格式有误')])
    parent = StringField('parent', validators=[Regexp(r'^[\d\w]{24,26}$', re.RegexFlag.I, 'parent格式有误')])
    flag = BooleanField('flag')
    title = StringField('title', validators=[Regexp(r'^[\d\w-]+$', re.RegexFlag.I, 'title格式有误')])