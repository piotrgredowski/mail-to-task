import smtplib
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

    def __init__(self, *, address, password, server_address, port):
        self.address = address
        self.server_address = server_address
        self.port = port

        self.server = smtplib.SMTP(server_address, port)
        self.context = ssl.create_default_context()

        self.server.ehlo()
        self.server.starttls(context=self.context)
        self.server.ehlo()

        self._server_login(address, password)

    def _server_login(self, sender_email, password):
        self.server.login(sender_email, password)

    def send(self, *, to, subject, msg):
        msg = MSG_TEMPLATE.format(subject=subject, content=msg)
        self.server.sendmail(self.address, to, msg)

    def stop(self):
        self.server.quit()
