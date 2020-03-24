import os
import ssl
from datetime import timedelta
from time import sleep

from trello import TrelloApi

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

while True:
    print("Alive")
    mails = receiver.get_not_seen_messages(mark_as_seen=True)
    from pprint import pprint

    pprint(mails)
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

    sleep(5)
