import os
import uuid

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from Dmail.email_base import EmailBase


class MimeMixin(EmailBase):
    def __init__(self, sender_email, *args, **kwargs):
        self.email_content = None
        self.sess_uuid = None
        super(MimeMixin, self).__init__(*args, sender_email=sender_email, **kwargs)

    def start(self):
        # message
        self.email_content = MIMEMultipart()
        self.email_content["From"] = self.sender_email
        self.sess_uuid = uuid.uuid1()
        super(MimeMixin, self).start()

    def quit(self):
        self.email_content = None
        self.sess_uuid = None
        super(MimeMixin, self).quit()

    # functionality
    def _get_email_content(self, email_text, email_recipient, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        if subject:
            self.email_content["Subject"] = subject
        if cc:
            self.email_content['cc'] = cc
        if bcc:
            self.email_content["Bcc"] = bcc
        self.email_content["To"] = email_recipient
        attachments and self.add_attachments(attachments)
        self.add_text(email_text, subtype=subtype)
        return self.email_content.as_string()

    def add_text(self, text, subtype):
        self.email_content.attach(MIMEText(text, subtype))

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

    def add_attachment(self, file_path, filename=None):
        with open(file_path, "rb") as attachment:
            # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename or os.path.basename(file_path)}",
        )
        self.email_content.attach(part)

    def add_image(self, img_path):
        path = os.path.abspath(img_path)
        with open(path, 'rb') as fp:
            img = MIMEImage(fp.read())

        img_uuid = str(uuid.uuid3(self.sess_uuid, path))
        img.add_header('Content-ID', f"<{img_uuid}>")
        self.email_content.attach(img)
        return img_uuid
