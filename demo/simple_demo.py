#!/usr/bin/python
# -*- coding:utf-8 -*-

from earo.event import Event, Field
from earo.app import App
from earo.config import Config
from earo.handler import Emittion, NoEmittion
import random
import time

class MyEventA(Event):
    __tag__ = 'my_event_tag'
    __description__ = 'my_event_description'
    my_field_one = Field(str, 'test')
    my_field_two = Field(int, 100)

class MyEventB(Event):
    pass

config = Config(
        app_name='My First App',
        source_event_cls=(MyEventA,),
        processors_tag_regex=['^my_event_tag$', '.*'],
        dashboard_host='0.0.0.0',
        dashboard_port=9527)

app = App(config)

@app.handler(MyEventA, derivative_events=[MyEventB])
def my_event_a_handler(context, event):

    time.sleep(random.random())

    print event. my_field_one
    print event. my_field_two

    choice = random.choice([0, 1])
    if choice == 0:
        return Emittion(MyEventB())
    else:
        return NoEmittion(MyEventB , 'choice == 1')

@app.handler(MyEventB)
def my_event_b_handler(context, event):

    time.sleep(random.random())

    choice = random.choice([0, 1])
    if choice == 0:
        return
    else:
        1 / 0

app.run_dashboard(True)

while True:
    time.sleep(10)
    app.emit(MyEventA())
