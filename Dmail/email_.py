import re

import markdown

from Dmail.email_base import EmailBase


class Email(EmailBase):
    _img_regex = re.compile(r'(!\[.*?\]\()(.*?)(\))')

    def __init__(self, mail_server, mail_port, sender_email=None, sender_password=None,
                 mail_use_tls=True, md_extensions=None):
        super().__init__(mail_server=mail_server, mail_port=mail_port, sender_email=sender_email,
                         sender_password=sender_password, mail_use_tls=mail_use_tls)
        self._markdown = markdown.Markdown(extensions=md_extensions or ['tables', 'fenced_code', 'footnotes'])

    def _process_message(self, message, subtype):
        if subtype == 'md':
            subtype = 'html'
            message = self._img_regex.sub(lambda match:
                                          f"{match.group(1)}cid:{self.add_image(match.group(2))}{match.group(3)}",
                                          message)
            message = self._markdown.convert(message)
        return super(Email, self)._process_message(message, subtype)

    def send_message(self, message, receiver_email, subject=None, cc=None, bcc=None, subtype='md', attachments=None):
        super(Email, self).send_message(message=message, receiver_email=receiver_email, subject=subject, cc=cc, bcc=bcc,
                                        subtype=subtype, attachments=attachments)
