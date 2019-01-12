#!/usr/bin/env python
from setuptools import setup

setup(
    name="see2",
    version="0.0.1",
    description="See2.io prototype using Enron email data",
    packages=find_packages(),
    scripts=['manage.py'],
    install_requires=[
        'Django==2.2.dev20190101154022',
        'numpy==1.15.4',
        'pandas==0.23.4',
        'python-dateutil==2.7.5',
        'pytz==2018.7',
        'simpy==3.0.11'
        'six==1.12.0',
        'sqlparse==0.2.4',
    ],
)