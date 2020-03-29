import os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from Dmail.mixin.mime_base_mixin import MimeBaseMixin


class MimeMixin(MimeBaseMixin):
    def start(self):
        self.email_content = MIMEMultipart()
        super(MimeMixin, self).start()

    def quit(self):
        self.email_content = None
        super(MimeMixin, self).quit()

    # functionality
    def _set_header(self, email_recipient=None, subject=None, cc=None, bcc=None, **kwargs):
        self.email_content["From"] = self.sender_email
        if subject:
            self.email_content["Subject"] = subject
        if cc:
            self.email_content['cc'] = ','.join(self._recipient_to_list(cc))
        if email_recipient:
            self.email_content["To"] = ','.join(self._recipient_to_list(email_recipient))

    def _get_converted_email_content(self):
        return self.email_content.as_string()

    def _add_text(self, text, subtype):
        self.email_content.attach(MIMEText(text, subtype))

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
        with open(img_path, 'rb') as fp:
            img = MIMEImage(fp.read())
        img_uuid = super(MimeMixin, self).add_image(img_path)
        img.add_header('Content-ID', f"<{img_uuid}>")
        self.email_content.attach(img)
        return img_uuid
