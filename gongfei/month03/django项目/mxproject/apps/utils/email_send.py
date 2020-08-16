# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：      email_semd
   Description :     
   Author :         gongyan
   Date：           2019/5/6
   Change Activity: 2019/5/6 19:34
-------------------------------------------------
"""
from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from mxproject.settings import EMAIL_FROM


def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title = 'teduz注册激活邮件！'
        email_body = '请点击一下链接激活您的账号：' \
                     'http://127.0.0.1:8000/acticve/{}'.format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '这是一封找回密码的邮件！'
        email_body = '请点击下面的链接重置您的密码：' \
                     'http://127.0.0.1:8000/reset/{}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'update_email':
        email_title = '这是一封邮箱修改验证码邮件！'
        email_body = '您的邮箱验证码为：{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass






def random_str(randomlength=8):
    str = ""
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0,length)]
    return str

