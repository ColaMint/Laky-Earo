#!/usr/bin/python
# -*- coding:utf-8 -*-

from earo.event import Event, Field

class RegisterEvent(Event):
    __tag__ = 'user.register'
    __description__ = '请求注册'

    username = Field(str)
    password = Field(str)

class UsernamePassCheckEvent(Event):
    __tag__ = 'user.username_pass_check'
    __description__ = '用户名通过检查'

class RegisterSuccessEvent(Event):
    __tag__ = 'user.register_success'
    __description__ = '注册成功'

    username = Field(str)
