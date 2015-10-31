# -*- coding:utf-8 -*-  

class MissingCurrentEvent(Exception):

    def __str__(self):
        return 'Missing current event.'

class MissingCurrentApp(Exception):

    def __str__(self):
        return 'Missing current app.'
