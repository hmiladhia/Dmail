import warnings

from abc import ABC
from pathlib import Path


class EmailBase(ABC):
    default_subtype = 'plain'

    def __init__(self, sender_email):
        self.sender_email = sender_email

    # interface
    def start(self):
        pass

    def quit(self):
        pass

    def send(self, email_text, to=None, subject=None, cc=None, bcc=None, subtype=None, attachments=None, sender=None):
        subtype = subtype or self.default_subtype
        self._pre_send(email_text, to=to, subject=subject, cc=cc, bcc=bcc, subtype=subtype, attachments=attachments)
        email_recipients = self._get_email_recipients(to, cc=cc, bcc=bcc)
        email_body = self.get_message(email_text, to=to, subject=subject, cc=cc, bcc=bcc,
                                      subtype=subtype, attachments=attachments, sender=sender)
        self.sendmail(email_recipients, email_body)
        self._post_send(email_text, to=to, subject=subject, cc=cc, bcc=bcc, subtype=subtype, attachments=attachments)

    def send_from_file(self, txt_file, to=None, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        message = Path(txt_file).read_text()
        self.send(message, to=to, subject=subject, cc=cc, bcc=bcc, subtype=subtype, attachments=attachments)

    # functionality
    def _pre_send(self, email_text=None, to=None, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        pass

    def _post_send(self, email_text, to=None, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        pass

    def sendmail(self, recipients, message):
        pass

    def get_message(self, email_text=None, to=None, subject=None, cc=None, bcc=None,
                    subtype=None, attachments=None, sender=None):
        email_body = f"""\
        Subject: {subject}
        To: {to}
        From: {self.sender_email}
        {email_text}"""
        return email_body

    # context manager
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    # utils
    @classmethod
    def _get_email_recipients(cls, to, cc=None, bcc=None):
        return cls._recipient_to_list(to) + cls._recipient_to_list(cc) + cls._recipient_to_list(bcc)

    @staticmethod
    def _recipient_to_list(recipient):
        if isinstance(recipient, str):
            return [recipient]
        elif recipient is None:
            return []
        else:
            return recipient

    # depreciated
    def send_message(self, message, receiver_email, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        warnings.warn("send_message() is deprecated; use send().", PendingDeprecationWarning)
        self.send(message, receiver_email, subject=subject, cc=cc, bcc=bcc, subtype=subtype, attachments=attachments)

    def send_message_from_file(self, message_file, receiver_email, subject=None, cc=None,
                               bcc=None, subtype=None, attachments=None):
        warnings.warn("send_message_from_file() is deprecated; use send_from_file().", PendingDeprecationWarning)
        self.send_from_file(message_file, receiver_email, subject=subject, cc=cc,
                            bcc=bcc, subtype=subtype, attachments=attachments)
