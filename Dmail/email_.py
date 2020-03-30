from Dmail import SimpleEmail
from Dmail.mixin import MarkdownMixin


class Email(SimpleEmail, MarkdownMixin):
    default_subtype = 'md'

    def __init__(self, mail_server, mail_port, sender_email=None, sender_credentials=None, mail_use_tls=True,
                 mail_use_ssl=False, md_extensions=None):
        super(Email, self).__init__(mail_server=mail_server, mail_port=mail_port, sender_email=sender_email,
                                    sender_credentials=sender_credentials, mail_use_tls=mail_use_tls,
                                    mail_use_ssl=mail_use_ssl, md_extensions=md_extensions)
