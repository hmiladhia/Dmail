import re

import markdown

from Dmail.mixin import HtmlMixin


class MarkdownMixin(HtmlMixin):
    # _img_regex = re.compile(r'(!\[.*?\]\()(.*?)(\))')

    def __init__(self, mail_server, mail_port, sender_email=None, sender_credentials=None,
                 mail_use_tls=True, mail_use_ssl=False, md_extensions=None):
        super(MarkdownMixin, self).__init__(mail_server=mail_server, mail_port=mail_port, sender_email=sender_email,
                                            sender_credentials=sender_credentials, mail_use_tls=mail_use_tls,
                                            mail_use_ssl=mail_use_ssl)
        self._markdown = markdown.Markdown(extensions=md_extensions or ['tables', 'fenced_code', 'footnotes'])

    def _process_text(self, text, subtype):
        if subtype == 'md':
            # text = self._img_regex.sub(self._md_add_img, text)
            text, subtype = self._markdown.convert(text), 'html'
        return super(MarkdownMixin, self)._process_text(text, subtype)
