import markdown

from Dmail.mixin import HtmlMixin


class MarkdownMixin(HtmlMixin):
    def __init__(self, sender_email=None, md_extensions=None, *args, **kwargs):
        super(MarkdownMixin, self).__init__(*args, sender_email=sender_email, **kwargs)
        self._markdown = markdown.Markdown(extensions=md_extensions or ['tables', 'fenced_code', 'footnotes'])

    def _process_text(self, text, subtype):
        if subtype == 'md':
            text, subtype = self._markdown.convert(text), 'html'
        return super(MarkdownMixin, self)._process_text(text, subtype)
