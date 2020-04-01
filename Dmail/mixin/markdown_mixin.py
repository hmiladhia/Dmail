import os.path as p

import markdown

from Dmail.mixin import HtmlMixin


class MarkdownMixin(HtmlMixin):
    def __init__(self, sender_email, md_extensions=None, styles=None, default_styles='default', wrapper_id=None, **kwargs):
        super(MarkdownMixin, self).__init__(sender_email=sender_email, **kwargs)
        self._markdown = markdown.Markdown(extensions=md_extensions or ['tables', 'fenced_code', 'footnotes'])
        self.styles = styles or []
        self.default_styles = default_styles
        self.wrapper_id = wrapper_id

    def _process_text(self, text, subtype, **kwargs):
        if subtype == 'md':
            kwargs.setdefault('alt_text', text)
            text, subtype = self._markdown.convert(text), 'html'
            text = self.__get_text_with_style(text)
        return super(MarkdownMixin, self)._process_text(text, subtype, **kwargs)

    def __get_text_with_style(self, text):
        styles = self.__get_styles()
        if styles:
            wrapper_start = f'<div id="{self.wrapper_id}">' if self.wrapper_id else ''
            wrapper_end = f'</div>' if self.wrapper_id else ''
            return (f'<html><head><style type="text/css">{styles}</style></head>'
                    f'<body>{wrapper_start}{text}{wrapper_end}</body></html>')
        else:
            return text

    def __get_styles(self):
        return '\n'.join(self.__load_styles(self.default_styles, default=True) + self.__load_styles(self.styles))

    @classmethod
    def __load_styles(cls, styles, default=False):
        if isinstance(styles, str):
            path = p.abspath(p.join(p.dirname(__file__), '..', 'styles', f'{styles.lower()}.css') if default else styles)
            with open(path, 'r') as css_file:
                style = css_file.read()
            return [style]
        else:
            s = []
            for style in styles:
                s.extend(cls.__load_styles(style))
            return s
