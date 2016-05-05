#!/usr/bin/python
# -*- coding:utf-8 -*-

from earo.app import App
from earo.config import Config
from event import RegisterEvent

config = Config(
        app_name='Register Demo',
        source_event_cls=(RegisterEvent,),
        processors_tag_regex=['^user.*', '.*'])

app = App(config)
