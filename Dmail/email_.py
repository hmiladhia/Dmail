import os
import re

import markdown

from Dmail.email_base import EmailBase


class Email(EmailBase):
    _img_regex = re.compile(r'(!\[.*?\]\()(.*?)(\))')
    _tld_regex = (r"(aero|asia|biz|cat|com|coop|edu|gov|info|int"
                  r"|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as"
                  r"|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg"
                  r"|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj"
                  r"|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu"
                  r"|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li"
                  r"|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mn|mn|mo|mp|mr|ms|mt|mu|mv|mw|mx|my|mz|na"
                  r"|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|nom|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ra"
                  r"|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th"
                  r"|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|"
                  r"yu|za|zm|zw|arpa)")
    _url_regex = re.compile(r"((https?|ftp)://)?(([\w_-]+\.)+"
                            f"{_tld_regex}"
                            r"(:\d+)?((/([~\w#+%@./_-]+))?(\?[\w+%@&\[\];=_-]+)?)?)")

    def __init__(self, mail_server, mail_port, sender_email=None, sender_password=None,
                 mail_use_tls=True, md_extensions=None):
        super().__init__(mail_server=mail_server, mail_port=mail_port, sender_email=sender_email,
                         sender_password=sender_password, mail_use_tls=mail_use_tls)
        self._markdown = markdown.Markdown(extensions=md_extensions or ['tables', 'fenced_code', 'footnotes'])

    def _process_message(self, message, subtype):
        if subtype == 'md':
            subtype = 'html'
            message = self._img_regex.sub(self.__md_add_img, message)
            message = self._markdown.convert(message)
        return super(Email, self)._process_message(message, subtype)

    def __md_add_img(self, match):
        file = match.group(2)
        if self._url_regex.fullmatch(file):
            return f"{match.group(1)}{file}{match.group(3)}"
        return f"{match.group(1)}cid:{self.add_image(file)}{match.group(3)}"

    def send_message(self, message, receiver_email, subject=None, cc=None, bcc=None, subtype='md', attachments=None):
        super(Email, self).send_message(message=message, receiver_email=receiver_email, subject=subject, cc=cc, bcc=bcc,
                                        subtype=subtype, attachments=attachments)
