import os
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
        self.server.quit()

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

    def send_message(self, message, receiver_email, subject=None, bcc=None):
        self.message["To"] = receiver_email
        if subject:
            self.message["Subject"] = subject
        if bcc:
            self.message["Bcc"] = bcc  # Recommended for mass emails
        self.message.attach(MIMEText(message, "plain"))
        self.server.sendmail(self.sender_email, receiver_email, self.message.as_string())
