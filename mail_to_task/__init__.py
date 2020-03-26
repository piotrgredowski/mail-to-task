import asyncio
import os
import ssl
from datetime import datetime, timedelta
from time import sleep

import requests
from flask import Flask
from rq_scheduler import Scheduler
from trello import TrelloApi

from jobs_queue import queue, redis_conn
from lib.config import config
from lib.mailer import MailReceiver, MailSender

trello = TrelloApi(config.secure.trello.api_key)
trello_token = os.environ.get("TRELLO_TOKEN")
trello.set_token(trello_token)

ssl_context = ssl.create_default_context()

mailer = MailSender(
    address=config.secure.sender.address,
    password=config.secure.sender.password,
    server_address=config.secure.sender.server_address,
    port=config.secure.sender.server_port,
    ssl_context=ssl_context,
)
receiver = MailReceiver(
    address=config.secure.sender.address,
    password=config.secure.sender.password,
    server_address=config.secure.sender.server_address,
    ssl_context=ssl_context,
)


def scan_inbox():
    mails = receiver.get_not_seen_messages(mark_as_seen=True)

    member_name = config.tasks[0].handler.options.assignee
    board_name = config.tasks[0].handler.options.board
    list_name = config.tasks[0].handler.options.list_name

    boards = trello.members.get_board(member_name)
    the_board = list(filter(lambda b: b["name"] == board_name, boards))[0]
    the_board_id = the_board["id"]

    lists = trello.boards.get_list(the_board_id)
    try:
        the_list_id = list(filter(lambda l: l["name"] == list_name, lists))[0]["id"]
    except IndexError:
        the_list_id = trello.boards.new_list(the_board_id, list_name)["id"]

    for mail in mails:
        trello.cards.new(
            name=mail.subject,
            idList=the_list_id,
            due=mail.date + timedelta(days=7),
            desc=mail.body,
        )


def ping_me():
    print("ping")
    requests.get(os.environ.get("APP_ADDRESS"))


scheduler = Scheduler(connection=redis_conn)
# scheduler = Scheduler(queue=queue)
scheduler.schedule(
    scheduled_time=datetime.utcnow() + timedelta(5),
    func=ping_me,
    interval=60,
    repeat=None,
)
scheduler.schedule(
    scheduled_time=datetime.utcnow(), func=scan_inbox, interval=5, repeat=None,
)
# breakpoint()

app = Flask("keep_me_alive")


@app.route("/", methods=["GET"])
def keep_me_alive():
    return "ok"


is_debug = os.environ.get("ENVIRONMENT") == "dev"

if __name__ == "__main__":
    app.run(debug=is_debug)
