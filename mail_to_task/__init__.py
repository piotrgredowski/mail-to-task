import os
import ssl

from flask import Flask, request
import requests
from trello import TrelloApi

from lib.config import config, Config
from lib.mailer import MailSender, MailReceiver


class MyFlask(Flask):
    cfg: Config = None
    mailer: MailSender = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


app_name = "mail_to_task"
app = MyFlask(app_name)
app.cfg = config

context = ssl.create_default_context()
app.mailer = MailSender(
    address=app.cfg.secure.sender.address,
    password=app.cfg.secure.sender.password,
    server_address=app.cfg.secure.sender.server_address,
    port=app.cfg.secure.sender.server_port,
    context=context,
)

receiver = MailReceiver(
    address=app.cfg.secure.sender.address,
    password=app.cfg.secure.sender.password,
    server_address=app.cfg.secure.sender.server_address,
)

a = receiver._get_unseen()
breakpoint()

trello = TrelloApi(app.cfg.secure.trello.api_key)
trello_token = os.environ.get("TRELLO_TOKEN")
trello.set_token(trello_token)


@app.route("/", methods=["POST"])
def main():
    target = request.args.get("target")

    if not target:
        return 400

    raise Exception(request.json)
    msg = request.json["plain"].strip()

    return "ok"


is_debug = os.environ.get("ENVIRONMENT") == "dev"

if __name__ == "__main__":
    app.run(debug=is_debug)
