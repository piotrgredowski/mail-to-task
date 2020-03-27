from rq import Queue
from redis import Redis

redis_conn = Redis(host="redis", port=6379)
queue = Queue(connection=redis_conn)
