import os
import smtplib
import ssl
import uuid

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class EmailBase:
    def __init__(self, mail_server, mail_port=None, sender_email=None, sender_password=None,
                 mail_use_tls=True, mail_use_ssl=False):
        self._check_sanity(mail_server, mail_port, sender_email, sender_password, mail_use_tls, mail_use_ssl)

        # server info
        self.server = None
        self.mail_server = mail_server
        self.mail_port = mail_port
        self.mail_use_tls = mail_use_tls
        self.mail_use_ssl = mail_use_ssl

        # login info
        self.sender_email = sender_email
        self.sender_password = sender_password

        # message init
        self.message = None
        self.sess_uuid = None

    def start(self, sender_email=None, sender_password=None):
        # server
        self.server = self.get_server(self.mail_server, self.mail_port, self.mail_use_tls, self.mail_use_ssl)

        # login
        sender_email = sender_email or self.sender_email
        sender_password = sender_password or self.sender_password
        if sender_password:
            self.server.login(sender_email, sender_password)

        # message
        self.message = MIMEMultipart()
        self.message["From"] = sender_email
        self.sess_uuid = uuid.uuid1()

    def quit(self, exc_type=None, exc_val=None, exc_tb=None):
        self.message = None
        self.sess_uuid = None
        self.server.quit()

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

    def send_message_from_file(self, message_file, receiver_email, subject=None, cc=None,
                               bcc=None, subtype='plain', attachments=None):
        with open(message_file, 'r') as f:
            message = f.read()
        self.send_message(message, receiver_email, subject=subject, cc=cc, bcc=bcc,
                          subtype=subtype, attachments=attachments)

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

    def add_image(self, img_path):
        path = os.path.abspath(img_path)
        with open(path, 'rb') as fp:
            img = MIMEImage(fp.read())

        img_uuid = str(uuid.uuid3(self.sess_uuid, path))
        img.add_header('Content-ID', f"<{img_uuid}>")
        self.message.attach(img)
        return img_uuid

    def add_message(self, message, subtype):
        message, subtype = self._process_message(message, subtype)
        self._add_message(message, subtype)

    def _add_message(self, message, subtype):
        self.message.attach(MIMEText(message, subtype))

    def _process_message(self, message, subtype):
        return message, subtype

    @staticmethod
    def get_server(mail_server, mail_port, mail_use_tls, mail_use_ssl):
        if mail_use_ssl:
            context = ssl.create_default_context()
            return smtplib.SMTP_SSL(mail_server, mail_port, context=context)
        else:
            server = smtplib.SMTP(mail_server, mail_port)
            if mail_use_tls:
                server.ehlo()
                server.starttls()
                server.ehlo()
            return server

    @staticmethod
    def _check_sanity(mail_server, mail_port, sender_email, sender_password, mail_use_tls, mail_use_ssl):
        if mail_use_ssl and mail_use_tls:
            raise ValueError("Can't use TLS and SSL at the same time")

    def __enter__(self, sender_email=None, sender_password=None):
        self.start(sender_email, sender_password)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit(exc_type, exc_val, exc_tb)
