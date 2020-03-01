from Dmail import Email
from Utils.configmanager import import_config


class Gmail(Email):
    def __init__(self, sender_email_id, sender_email_id_password):
        config = import_config('Dmail.config.GmailConfig')
        super(Gmail, self).__init__(**config, sender_email_id=sender_email_id,
                                    sender_email_id_password=sender_email_id_password)
