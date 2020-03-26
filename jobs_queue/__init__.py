from rq import Queue
from redis import Redis

redis_conn = Redis(host="redis", port=6379)
queue = Queue("1", connection=redis_conn)
