import os

from Dmail import Email
from Utils.configmanager import ConfigManager


class Gmail(Email):
    def __init__(self, sender_email_id, sender_email_id_password):
        cm = ConfigManager(default_path=os.path.join(os.path.dirname(__file__), 'config'))
        config = cm.load_config('GmailConfig')
        super(Gmail, self).__init__(**config, sender_email_id=sender_email_id,
                                    sender_email_id_password=sender_email_id_password)
