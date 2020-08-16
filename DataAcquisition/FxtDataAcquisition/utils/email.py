# -*- coding: utf-8 -*-
# @Time    : 18-10-31 上午10:16
# @Author  : luomingming

import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from FxtDataAcquisition.settings import EMAIL

logger = logging.getLogger(__name__)

hostname = EMAIL['host']
port = EMAIL['port']
sender = EMAIL['username']
password = EMAIL['password']
receivers = EMAIL['receivers']


def send(msg, subject):
    try:
        message = MIMEText(msg, 'plain', 'utf-8')
        message['Subject'] = subject
        message['From'] = Header(sender, 'utf-8')
        message['To'] = receivers

        smtp_obj = smtplib.SMTP_SSL(hostname, port=port)
        smtp_obj.login(sender, password)
        smtp_obj.sendmail(from_addr=sender, to_addrs=receivers.split(','), msg=message.as_string())
        smtp_obj.quit()
        logger.info('email send success')
    except smtplib.SMTPException as e:
        logger.error('error: can not send email, {}'.format(e))
