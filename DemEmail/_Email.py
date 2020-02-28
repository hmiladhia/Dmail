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


if __name__ == "__main__":
    import os
    from Utils.configmanager import ConfigManager
    # list of email_id to send the mail
    receiver = "***REMOVED***"
    cm = ConfigManager(default_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config'))
    config = cm.load_config('GmailConfig')
    email_id = os.environ.get('mail')
    password = os.environ.get('pass')
    with Email(**config, sender_email_id=email_id, sender_email_id_password=password) as gmail:
        gmail.send_message("Love1", receiver, "I love you man")
        gmail.send_message("Love2", receiver, "I love you man")
