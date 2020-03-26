import re

import markdown

from Dmail.email_base import EmailBase


class Email(EmailBase):
    _img_regex = re.compile(r'(!\[.*?\]\()(.*?)(\))')
    _markdown = markdown.Markdown(extensions=['tables'])

    def _process_message(self, message, subtype):
        if subtype == 'md':
            subtype = 'html'
            message = self._img_regex.sub(lambda match:
                                          f"{match.group(1)}cid:{self.add_image(match.group(2))}{match.group(3)}",
                                          message)
            message = self._markdown.convert(message)
        return super(Email, self)._process_message(message, subtype)
