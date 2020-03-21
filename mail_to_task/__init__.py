import os

from flask import Flask, request
import requests

from lib.config import config, Config
from lib.mailer import MailSender


class MyFlask(Flask):
    cfg: Config = None
    mailer: MailSender = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


app = MyFlask("mail_to_task")
app.cfg = config
app.mailer = MailSender(
    address=app.cfg.secure.sender.address,
    password=app.cfg.secure.sender.password,
    server_address=app.cfg.secure.sender.server_address,
    port=app.cfg.secure.sender.server_port,
)


@app.route("/", methods=["POST"])
def main():
    target = request.args.get("target")

    if not target:
        return 400

    receiver = app.cfg.secure.trello.address

    msg = request.json["plain"].strip()

    app.mailer.send(to=receiver, msg=msg.encode("utf-8"))
    return "ok"


is_debug = os.environ.get("ENVIRONMENT") == "dev"

if __name__ == "__main__":
    app.run(debug=is_debug)
