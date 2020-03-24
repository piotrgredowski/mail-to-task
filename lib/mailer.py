import smtplib
import imaplib
import email
import ssl
from ssl import SSLContext


MSG_TEMPLATE = """
Subject: {subject}

{content}
"""


class MailSender:
    address: str
    server_address: str
    port: int

    context: SSLContext
    server: smtplib.SMTP

    def __init__(self, *, address, password, server_address, port, context):
        self.address = address
        self.server_address = server_address
        self.port = port

        self.server = smtplib.SMTP(server_address, port)
        # self.context = ssl.create_default_context()

        self.server.ehlo()
        self.server.starttls(context=context)
        self.server.ehlo()

        self._server_login(address, password)

    def _server_login(self, sender_email, password):
        self.server.login(sender_email, password)

    def send(self, *, to, subject, msg):
        msg = MSG_TEMPLATE.format(subject=subject, content=msg)
        self.server.sendmail(self.address, to, msg)

    def stop(self):
        self.server.quit()


class MailReceiver:
    address: str
    server_address: str
    port: int

    context: SSLContext
    server: imaplib.IMAP4_SSL

    def __init__(self, *, address, password, server_address):
        self.address = address
        self.server_address = server_address
        # self.port = port
        self.server = imaplib.IMAP4_SSL(server_address)

        self._server_login(address, password)

    def _server_login(self, receiver_email, password):
        self.server.login(receiver_email, password)

    def _get_unseen(self):
        self.server.select("INBOX")
        status, data = self.server.search(None, "ALL")

        if status == "OK":
            mail_ids = []
            for block in data:
                mail_ids += block.split()

            mails = []
            for mail_id in mail_ids:
                status, msg = self.server.fetch(mail_id, "(RFC822)")
                if status == "OK":
                    for response_part in msg:
                        if isinstance(response_part, tuple):
                            mail = email.message_from_bytes(response_part[1])
                            mails += mail
            breakpoint()
