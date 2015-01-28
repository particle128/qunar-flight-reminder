#!/usr/bin/env python
# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.charset import Charset

from config import *
# config_local.py will override the previous config.py
try:
    from config_local import *
except:
    pass

def get_message(text):
    msg = MIMEText(text, _charset='utf-8') 
    msg['From'] = FROM_ADDR
    msg['To'] = TO_ADDR
    msg['Subject'] = u'Qunar Notice'
    return msg

def send(message):
    try:
        smtp = smtplib.SMTP(MAIL_HOST) 
        smtp.login(MAIL_USER, MAIL_PWD)
        smtp.sendmail(FROM_ADDR, TO_ADDR, msg.as_string())
        print 'sending mail success.'
    except Exception as e:
        print e
    finally:
        smtp.quit()

def send_email(text):
    message = get_message(text)
    send(message)
