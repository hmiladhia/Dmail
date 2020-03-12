import os
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import markdown2


class Email:
    def __init__(self, mail_server, mail_port, sender_email=None, sender_password=None, mail_use_tls=True):
        self.server = smtplib.SMTP(mail_server, mail_port)
        self.sender_email = sender_email
        self.sender_password = sender_password

    def __enter__(self):
        self.server.starttls()
        self.server.login(self.sender_email, self.sender_password)
        self.message = MIMEMultipart()
        self.message["From"] = self.sender_email
        return self

    def __exit__(self, type, value, traceback):
        self.message = None
        self.server.quit()

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

        self.message.attach(part)

    def add_message(self, message, subtype):
        if subtype == 'md':
            subtype = 'html'
            message = f"""
                    <!doctype html>
                    <html>
                        <head>
                        </head>
                        <body>
                            {markdown2.markdown(message)}
                        </body>
                    </html>"""
        self.message.attach(MIMEText(message, subtype))

    def send_message(self, message, receiver_email, subject=None, cc=None, bcc=None, subtype='plain', attachments=None):
        if subject:
            self.message["Subject"] = subject
        if cc:
            self.message['cc'] = cc
        if bcc:
            self.message["Bcc"] = bcc
        self.add_message(message, subtype)
        if attachments:
            self.add_attachments(attachments)
        self.server.sendmail(self.sender_email, receiver_email, self.message.as_string())
