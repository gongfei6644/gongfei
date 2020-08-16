# -*- coding: utf-8 -*-

import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from app.config import EMAIL

logger = logging.getLogger(__name__)

hostname = EMAIL['host']
port = EMAIL['port']
sender = EMAIL['username']
password = EMAIL['password']
receivers = EMAIL['receivers']


def send(msg, subject):
    try:
        # message = MIMEText(msg, 'plain', 'utf-8')
        message = MIMEText(msg, 'html', 'utf-8')
        message['Subject'] = subject
        message['From'] = Header(sender, 'utf-8')
        message['To'] = receivers

        smtpObj = smtplib.SMTP_SSL(hostname, port=port)
        smtpObj.login(sender, password)
        smtpObj.sendmail(from_addr=sender, to_addrs=receivers.split(','), msg=message.as_string())
        smtpObj.quit()
        logger.info('email send success')
    except smtplib.SMTPException as e:
        logger.error('error: can not send email, {}'.format(e))
