#!/usr/bin/python
# -*- coding:utf-8 -*-
from setuptools import setup

setup(
    name='Earo',
    version='0.1.0',
    url='https://github.com/Everley1993/Laky-Earo',
    license='Apache',
    author='Everley',
    author_email='463785757@qq.com',
    description='A microframework based on EDA for business logic development.',
    packages=['earo'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'flask',
        'enum',
        'atomic',
    ]
)
