#!/usr/bin/python
# -*- coding:utf-8 -*-

def datetime_delta_ms(d1, d2):
    delta = d1 - d2
    return  delta.days * 24 * 3600 * 1000 + \
            delta.seconds * 1000 + \
            delta.microseconds / 1000;
