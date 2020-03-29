import mimetypes
import os

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

from Dmail.mixin.mime_base_mixin import MimeBaseMixin


class MimeMixin(MimeBaseMixin):
    def new_message(self):
        self.message = MIMEMultipart()

    def quit(self):
        self.message = None
        super(MimeMixin, self).quit()

    def _set_header(self, to=None, subject=None, cc=None, bcc=None, **kwargs):
        self.__add_header("From", self.sender_email)
        self.__add_header('Subject', subject)
        self.__add_header('cc', ','.join(self._recipient_to_list(cc)))
        self.__add_header("To", ','.join(self._recipient_to_list(to)))

    def _get_converted_email_content(self):
        return self.message.as_string()

    def _add_text(self, text, subtype):
        self.message.attach(MIMEText(text, subtype))

    def add_attachment(self, file_path, filename=None):
        content_type, encoding = mimetypes.guess_type(file_path)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)

        with open(file_path, 'r' if main_type == 'text' else 'rb') as fp:
            content = fp.read()

        if main_type == 'text':
            part = MIMEText(content, _subtype=sub_type)
        elif main_type == 'image':
            part = MIMEImage(content, _subtype=sub_type)
        elif main_type == 'audio':
            part = MIMEAudio(content, _subtype=sub_type)
        else:
            part = MIMEBase(main_type, sub_type)
            part.set_payload(content)
            encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment', filename=filename or os.path.basename(file_path))

        self.message.attach(part)

    def add_image(self, img_path):
        with open(img_path, 'rb') as fp:
            img = MIMEImage(fp.read())
        img_uuid = super(MimeMixin, self).add_image(img_path)
        img.add_header('Content-ID', f"<{img_uuid}>")
        self.message.attach(img)
        return img_uuid

    def __add_header(self, key, value):
        if value:
            try:
                self.message.replace_header(key, value)
            except KeyError:
                self.message.add_header(key, value)
