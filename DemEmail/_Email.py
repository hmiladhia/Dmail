import smtplib


class Email:
    def __init__(self, mail_server, mail_port, sender_email_id=None, sender_email_id_password=None, mail_use_tls=True):
        self.server = smtplib.SMTP(mail_server, mail_port)
        self.sender_email_id = sender_email_id
        self.sender_email_id_password = sender_email_id_password

    def __enter__(self):
        self.server.starttls()
        self.server.login(self.sender_email_id, self.sender_email_id_password)
        return self

    def __exit__(self, type, value, traceback):
        self.server.quit()

    def send_message(self, message, receiver_id, subject=None):
        if subject:
            message = 'Subject: {}\n\n{}'.format(subject, message)
        self.server.sendmail(self.sender_email_id, receiver_id, message.encode("utf8"))