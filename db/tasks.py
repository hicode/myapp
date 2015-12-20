# coding=utf-8

#from gevent import monkey
#monkey.patch_socket()

from celery import Celery

BROKER_URL = 'redis://localhost:6379/2'
celery = Celery('tasks', broker=BROKER_URL)

@celery.task
def add(x, y):
    return x + y
