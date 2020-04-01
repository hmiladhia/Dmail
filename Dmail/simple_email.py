from Dmail.mixin import HtmlMixin, MimeMixin, SmtpMixin


class SimpleEmail(HtmlMixin, MimeMixin, SmtpMixin):
    pass
