import os
import ssl

# xxx = queue.enqueue(x)
# job_1 = queue.enqueue(ping_me, os.environ.get("APP_ADDRESS"))
# job_1 = queue.enqueue(
#     scan_inbox,
#     args=[
#         address,
#         password,
#         server_address,
#         member_name,
#         board_name,
#         list_name,
#         trello,
#     ],
# )
from datetime import datetime, timedelta

from flask import Flask
from trello import TrelloApi

from jobs_queue import queue

from jobs_queue.register_tasks import ping_me, scan_inbox
from jobs_queue.scheduler import scheduler
from lib.config import config

# register_tasks()

address = config.secure.sender.address
password = config.secure.sender.password
server_address = config.secure.sender.server_address

member_name = config.tasks[0].handler.options.assignee
board_name = config.tasks[0].handler.options.board
list_name = config.tasks[0].handler.options.list_name

trello = TrelloApi(config.secure.trello.api_key)
trello_token = os.environ.get("TRELLO_TOKEN")
trello.set_token(trello_token)
# receiver = MailReceiver(
#     address=address, password=password, server_address=server_address,
# )

# queue.enqueue(
#     scan_inbox,
#     address,
#     password,
#     server_address,
#     member_name,
#     board_name,
#     list_name,
#     trello,
# )
# queue.enqueue(ping_me, os.environ.get("APP_ADDRESS"))

list_of_job_instances = scheduler.get_jobs()
for job in list_of_job_instances:
    scheduler.cancel(job)

scheduler.schedule(
    scheduled_time=datetime.utcnow(),
    func=ping_me,
    args=[os.environ.get("APP_ADDRESS")],
    interval=60 * 25,
    result_ttl=60 * 25 + 1,
    repeat=None,
)
job = scheduler.schedule(
    scheduled_time=datetime.utcnow(),
    func=scan_inbox,
    args=[
        address,
        password,
        server_address,
        member_name,
        board_name,
        list_name,
        trello,
    ],
    result_ttl=16,
    interval=15,
    repeat=None,
)
# scheduler.enqueue_in(timedelta(minutes=1), ping_me, os.environ.get("APP_ADDRESS"))


app = Flask("keep_me_alive")


@app.route("/", methods=["GET"])
def keep_me_alive():
    return "ok"


is_debug = os.environ.get("ENVIRONMENT") == "dev"

if __name__ == "__main__":
    app.run(debug=is_debug, port=8191)
