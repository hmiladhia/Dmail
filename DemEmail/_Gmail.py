import os

from DemEmail import Email
from Utils.configmanager import ConfigManager


class Gmail(Email):
    def __init__(self, sender_email_id, sender_email_id_password):
        cm = ConfigManager(default_path=os.path.join(os.path.dirname(__file__), 'config'))
        config = cm.load_config('GmailConfig')
        super(Gmail, self).__init__(**config, sender_email_id=sender_email_id,
                                    sender_email_id_password=sender_email_id_password)


if __name__ == "__main__":
    # list of email_id to send the mail
    receiver = "***REMOVED***"
    email_id = os.environ.get('mail')
    password = os.environ.get('pass')
    with Gmail(email_id, password) as gmail:
        gmail.send_message("Love1", receiver, "I love you man")
        gmail.send_message("Love2", receiver, "I love you man")

