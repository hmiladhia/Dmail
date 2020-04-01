import pathlib

import markdown

from Dmail.mixin import HtmlMixin


class MarkdownMixin(HtmlMixin):
    def __init__(self, sender_email, md_extensions=None, styles=None, wrapper_id=None, **kwargs):
        super(MarkdownMixin, self).__init__(sender_email=sender_email, **kwargs)
        self._markdown = markdown.Markdown(extensions=md_extensions or ['tables', 'fenced_code', 'footnotes'])
        self.styles = styles or []
        self.wrapper_id = wrapper_id

    def _process_text(self, text, subtype, **kwargs):
        if subtype == 'md':
            kwargs.setdefault('alt_text', text)
            text, subtype = self._markdown.convert(text), 'html'
            text = self.__get_text_with_style(text)
        return super(MarkdownMixin, self)._process_text(text, subtype, **kwargs)

    def __get_text_with_style(self, text):
        styles = '\n'.join(self.__get_styles(self.styles))
        if styles:
            wrapper_start = f'<div id="{self.wrapper_id}">' if self.wrapper_id else ''
            wrapper_end = f'</div>' if self.wrapper_id else ''
            return (f'<html><head><style type="text/css">{styles}</style></head>'
                    f'<body>{wrapper_start}{text}{wrapper_end}</body></html>')
        else:
            return text

    @classmethod
    def __get_styles(cls, styles):
        if isinstance(styles, str):
            return [pathlib.Path(styles).read_text()]
        else:
            s = []
            for style in styles:
                s.extend(cls.__get_styles(style))
            return s
