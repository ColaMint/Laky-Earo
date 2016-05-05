#!/usr/bin/python
# -*- coding:utf-8 -*-

from app import app
from event import RegisterEvent, UsernamePassCheckEvent, RegisterSuccessEvent
from earo.handler import Emittion, NoEmittion
import time
import random

users = []

@app.handler(RegisterEvent, derivative_events=[UsernamePassCheckEvent], description='检查用户名')
def check_username(context, event):
    time.sleep(random.random())
    if event.username is None:
        return NoEmittion(UsernamePassCheckEvent, '`username` is None.')
    elif event.username in users:
        return NoEmittion(UsernamePassCheckEvent, '`username` existed.')
    else:
        return Emittion(UsernamePassCheckEvent(username=event.username))

@app.handler(UsernamePassCheckEvent, derivative_events=[RegisterSuccessEvent], description='进行注册')
def register(context, event):
    register_event = context.find_event(RegisterEvent)
    print 'create user(%s, %s)...' % (
        register_event.username, register_event.password)
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
