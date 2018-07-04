from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError


class Login(FlaskForm):
    username = StringField('username', validators=[DataRequired("please input username"), Length(1, 32)])
    password = PasswordField('password', validators=[DataRequired("please input password"), Length(6, 64)])
    vcode = StringField('vcode', validators=[DataRequired("please input vcode"), Length(4, 5)]) # 验证码

    def validate_vcode(self, value):
        """
        校验验证码
        """
        value = value.data
        vcode = session.get('vcode')

        # 验证后就设置实效
        session['vcode'] = None
        if not isinstance(vcode, str) or len(vcode) < 1 or vcode.lower() != value.lower():
            raise ValidationError("vcode error")