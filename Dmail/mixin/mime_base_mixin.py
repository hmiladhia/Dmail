import os
import uuid

from Dmail.mixin import EmailBase


class MimeBaseMixin(EmailBase):
    def __init__(self, sender_email, **kwargs):
        self.message = None
        self.sess_uuid = None
        self.recreate_message_after_send = True
        super(MimeBaseMixin, self).__init__(sender_email=sender_email, **kwargs)

    # interface
    def add_attachments(self, attachments, *args, **kwargs):
        if isinstance(attachments, str):
            self.add_attachment(attachments, *args, **kwargs)
        elif isinstance(attachments, dict):
            for filename, path in attachments.items():
                self.add_attachment(path, filename)
        elif hasattr(attachments, '__iter__'):
            for file_path in attachments:
                self.add_attachment(file_path)
        else:
            raise TypeError('attachments should either be of type str, dict or list')

    def add_text(self, text, subtype):
        text, subtype = self._process_text(text, subtype)
        self._add_text(text, subtype)

    def add_attachment(self, file_path, filename=None):
        pass

    def add_image(self, img_path):
        return self.__get_uuid(img_path)

    def new_message(self):
        pass

    def start(self):
        self.new_message()
        self.sess_uuid = uuid.uuid1()
        super(MimeBaseMixin, self).start()

    def quit(self):
        self.message = None
        self.sess_uuid = None
        super(MimeBaseMixin, self).quit()

    def get_message(self, email_text=None, to=None, subject=None, cc=None, bcc=None,
                    subtype=None, attachments=None, sender=None):
        self._set_header(to=to, subject=subject, cc=cc, bcc=bcc, sender=sender)
        self._add_message_content(email_text, subtype, attachments)
        return self._get_converted_message()

    # functionality
    def _add_message_content(self, email_text=None, subtype=None, attachments=None):
        attachments and self.add_attachments(attachments)
        email_text and self.add_text(email_text, subtype=subtype)

    def _get_converted_message(self):
        return self.message

    def _post_send(self, email_text, to=None, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        if self.recreate_message_after_send:
            self.new_message()

    def _set_header(self, to=None, subject=None, cc=None, bcc=None, sender=None, **kwargs):
        pass

    def _process_text(self, text, subtype):
        return text, subtype

    def _add_text(self, text, subtype):
        pass

    # private
    def __get_uuid(self, path):
        path = os.path.abspath(path)
        img_uuid = str(uuid.uuid3(self.sess_uuid, path))
        return img_uuid
