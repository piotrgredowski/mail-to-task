import os
import ssl

from flask import Flask

from jobs_queue import queue

# from lib.x import x
from jobs_queue.register_tasks import MailReceiver, ping_me, register_tasks, scan_inbox
from lib.config import config

# register_tasks()

# xxx = queue.enqueue(x)
# job_1 = queue.enqueue(ping_me, os.environ.get("APP_ADDRESS"))
job_1 = queue.enqueue(
    scan_inbox,
    kwargs={
        "address": config.secure.sender.address,
        "password": config.secure.sender.password,
        "server_address": config.secure.sender.server_address,
    },
)
# breakpoint()


app = Flask("keep_me_alive")


@app.route("/", methods=["GET"])
def keep_me_alive():
    return "ok"


is_debug = os.environ.get("ENVIRONMENT") == "dev"

if __name__ == "__main__":
    app.run(debug=is_debug, port=8191)
