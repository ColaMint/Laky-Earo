#!/usr/bin/python
# -*- coding:utf-8 -*-

from app import app
from event import RegisterEvent, UsernamePassCheckEvent, RegisterSuccessEvent, EmailPassCheckEvent
from earo.handler import Emittion, NoEmittion
import time
import random
import re

users = []

email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

@app.handler(RegisterEvent, derivative_events=[UsernamePassCheckEvent], description='检查用户名')
def check_username(context, event):
    time.sleep(random.random())
    if event.username is None:
        return NoEmittion(UsernamePassCheckEvent, '`username` is None.')
    elif event.username in users:
        return NoEmittion(UsernamePassCheckEvent, '`username` existed.')
    else:
        return Emittion(UsernamePassCheckEvent(username=event.username))

@app.handler(UsernamePassCheckEvent, derivative_events=[EmailPassCheckEvent], description='检查邮箱')
def check_email(context, event):
    register_event = context.find_event(RegisterEvent)
    time.sleep(random.random())
    if register_event.email is None:
        return NoEmittion(EmailPassCheckEvent, '`email` is None.')
    elif not email_regex.match(register_event.email):
        return NoEmittion(EmailPassCheckEvent, '`email` is invalid')
    else:
        return Emittion(EmailPassCheckEvent(email=register_event.email))


@app.handler(EmailPassCheckEvent, derivative_events=[RegisterSuccessEvent], description='进行注册')
def register(context, event):
    register_event = context.find_event(RegisterEvent)
    print 'create user(%s, %s, %s)...' % (
        register_event.username, register_event.email, register_event.password)
    time.sleep(random.random())
    users.append(register_event.username)
    return Emittion(RegisterSuccessEvent(username=register_event.username))

@app.handler(RegisterSuccessEvent, description='关注官方账号')
def follow_official_users(context, event):
    print '%s: follow official users...' % event.username
    time.sleep(random.random())

@app.handler(RegisterSuccessEvent, description='增加积分')
def add_points(context, event):
    print '%s: add 100 points' % event.username
    time.sleep(random.random())

@app.handler(RegisterSuccessEvent, description='发送邮件')
def send_email(context, event):
    email_pass_check_event = context.find_event(EmailPassCheckEvent)
    print '%s: send email to `%s`' % event.username, email_pass_check_event.email
    time.sleep(random.random())
