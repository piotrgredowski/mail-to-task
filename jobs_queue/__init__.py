import os

from rq import Queue
import redis

from worker import conn

queue = Queue(connection=conn)
