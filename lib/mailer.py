import email
import smtplib
import typing
from dataclasses import dataclass
from email.header import decode_header
from email.iterators import typed_subpart_iterator
from enum import Enum
from ssl import SSLContext

from imbox import Imbox

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

    def __init__(self, *, address, password, server_address, port, ssl_context):
        self.address = address
        self.server_address = server_address
        self.port = port

        self.server = smtplib.SMTP(server_address, port)
        # self.context = ssl.create_default_context()

        self.server.ehlo()
        self.server.starttls(context=ssl_context)
        self.server.ehlo()

        self._server_login(address, password)

    def _server_login(self, sender_email, password):
        self.server.login(sender_email, password)

    def send(self, *, to, subject, msg):
        msg = MSG_TEMPLATE.format(subject=subject, content=msg)
        self.server.sendmail(self.address, to, msg)

    def stop(self):
        self.server.quit()


class FLAGS(Enum):
    SEEN = "\\Seen"
    UNSEEN = "\\Unseen"


class Labels(Enum):
    SEEN_BY_DEV = "SEEN_BY_DEV"
    ALREADY_PROCESSED = "ALREADY_PROCESSED"


@dataclass
class ProcessedMessage:
    uid: int
    subject: str
    body: str
    date: str


class MailReceiver:
    address: str
    server_address: str
    port: int

    # context: SSLContext
    server: Imbox

    def __init__(self, *, address, password, server_address):
        # def __init__(self, *, address, password, server_address, ssl_context):
        self.address = address
        self.server_address = server_address
        # self.port = port
        self.server = Imbox(
            hostname=server_address,
            username=address,
            password=password,
            ssl=True,
            # ssl_context=ssl_context,
        )

    def _add_label(self, flag: FLAGS):
        pass

    def _get_charset(self, message, default="utf-8"):
        # Taken from
        # http://ginstrom.com/scribbles/2007/11/19/parsing-multilingual-email-with-python/
        """Get the message charset"""

        if message.get_content_charset():
            return message.get_content_charset()

        if message.get_charset():
            return message.get_charset()

        return default

    def _get_header(header_text, default="utf-8"):
        # Taken from
        # http://ginstrom.com/scribbles/2007/11/19/parsing-multilingual-email-with-python/
        """Decode the specified header"""

        headers = decode_header(header_text)
        header_sections = [str(text, charset or default) for text, charset in headers]
        return u"".join(header_sections)

    def _get_body(self, message):
        # Taken from
        # http://ginstrom.com/scribbles/2007/11/19/parsing-multilingual-email-with-python/
        """Get the body of the email message"""

        if message.is_multipart():
            # get the plain text version only
            text_parts = [
                part for part in typed_subpart_iterator(message, "text", "plain")
            ]
            body = []
            for part in text_parts:
                charset = self._get_charset(part, self._get_charset(message))
                body.append(str(part.get_payload(decode=True), charset, "replace"))

            return u"\n".join(body).strip()

        else:
            # if it is not multipart, the payload will be a string
            # representing the message body
            body = str(
                message.get_payload(decode=True), self._get_charset(message), "replace"
            )
            return body.strip()

    def _move_message_to_folder(self, mail_id: int, folder_name: str):
        # if folder_name not in self.server.folders:
        #     self.server.create_folder(folder_name)
        self.server.move(mail_id, folder_name)

    def get_not_seen_messages(
        self, mark_as_seen=False
    ) -> typing.List[ProcessedMessage]:
        messages = self.server.messages()

        mails: typing.List[ProcessedMessage] = []

        for uid, message_data in messages:
            # email_message = email.message_from_bytes(message_data[b"RFC822"])
            body = message_data.body["plain"]
            date = message_data.parsed_date
            subject = message_data.subject
            mails.append(
                ProcessedMessage(
                    uid=uid, body=body, subject=subject.replace("Re:", ""), date=date
                )
            )

            self._move_message_to_folder(uid, Labels.SEEN_BY_DEV.value)

        return mails
