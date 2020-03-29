from Dmail.simple_email import SimpleEmail
from Dmail.mixin.markdown_mixin import MarkdownMixin


class Email(SimpleEmail, MarkdownMixin):
    default_subtype = 'md'
