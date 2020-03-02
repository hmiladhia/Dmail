import smtplib


class Email:
    def __init__(self, mail_server, mail_port, sender_email=None, sender_password=None, mail_use_tls=True):
        self.server = smtplib.SMTP(mail_server, mail_port)
        self.sender_email = sender_email
        self.sender_password = sender_password

    def __enter__(self):
        self.server.starttls()
        self.server.login(self.sender_email, self.sender_password)
        return self

    def __exit__(self, type, value, traceback):
        self.server.quit()

    def send_message(self, message, receiver_id, subject=None):
        if subject:
            message = 'Subject: {}\n\n{}'.format(subject, message)
        self.server.sendmail(self.sender_email, receiver_id, message.encode("utf8"))