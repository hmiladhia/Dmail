from Dmail import SimpleEmail
from Dmail.mixin import MarkdownMixin


class Email(SimpleEmail, MarkdownMixin):
    default_subtype = 'md'
