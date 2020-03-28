import warnings

from abc import ABC
from pathlib import Path


class EmailBase(ABC):
    default_subtype = 'plain'

    def __init__(self, sender_email, *args, **kwargs):
        self.sender_email = sender_email

    # interface
    def start(self):
        pass

    def quit(self):
        pass

    def send(self, email_text, email_recipient, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        email_body = self._get_email_content(email_text, email_recipient, subject=subject, cc=cc, bcc=bcc,
                                             subtype=subtype or self.default_subtype, attachments=attachments)
        self._send_email(email_recipient, email_body)

    def send_from_file(self, txt_file, email_recipient, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        message = Path(txt_file).read_text()
        self.send(message, email_recipient, subject=subject, cc=cc, bcc=bcc, subtype=subtype, attachments=attachments)

    # functionality
    def _send_email(self, email_recipient, email_body):
        pass

    def _get_email_content(self, email_text, email_recipient, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        email_body = f"""\
        Subject: Hi Mailtrap
        To: {email_recipient}
        From: {self.sender_email}
        {email_text}"""
        return email_body

    def _process_text(self, email_text, subtype):
        return email_text, subtype

    # context manager
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    # depreciated
    def send_message(self, message, receiver_email, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        warnings.warn("send_message() is deprecated; use send().", PendingDeprecationWarning)
        self.send(message, receiver_email, subject=subject, cc=cc, bcc=bcc, subtype=subtype, attachments=attachments)

    def send_message_from_file(self, message_file, receiver_email, subject=None, cc=None,
                               bcc=None, subtype='plain', attachments=None):
        warnings.warn("send_message_from_file() is deprecated; use send_from_file().", PendingDeprecationWarning)
        self.send_from_file(message_file, receiver_email, subject=subject, cc=cc,
                            bcc=bcc, subtype=subtype, attachments=attachments)
