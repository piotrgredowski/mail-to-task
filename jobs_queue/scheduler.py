from datetime import datetime

from rq_scheduler import Scheduler

from worker import conn


# class Scheduler:
#     def __init__(self, connection):
#         self._scheduler = RqScheduler(connection=connection)

#     def schedule(self, func, interval, repeat, scheduled_time=datetime.utcnow()):
#         self._scheduler.schedule(
#             scheduled_time=scheduled_time, func=func, interval=interval, repeat=repeat,
#         )


scheduler = Scheduler(connection=conn)
