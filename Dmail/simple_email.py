from Dmail.mixin.smtp_mixin import SmtpMixin
from Dmail.mixin.mime_mixin import MimeMixin


class SimpleEmail(MimeMixin, SmtpMixin):
    pass
