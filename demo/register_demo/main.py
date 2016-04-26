#!/usr/bin/python
# -*- coding:utf-8 -*-

import handler
from app import app
from event import RegisterEvent
import random
import time

def random_username():
    return 'user_%s' % random.randint(1, 100)

if __name__ == '__main__':
    app.run_dashboard(True)
    while True:
        time.sleep(5)
        app.emit(RegisterEvent(username=random_username(), password='123456'))
