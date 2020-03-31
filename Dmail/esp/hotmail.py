from Dmail import Email


class Hotmail(Email):
    def __init__(self, sender_email, sender_credentials, mail_port=587, **kwargs):
        super(Hotmail, self).__init__(mail_server="smtp.live.com", mail_port=mail_port,
                                      sender_email=sender_email, sender_credentials=sender_credentials,
                                      mail_use_tls=(mail_port == 587), mail_use_ssl=(mail_port == 465), **kwargs)
