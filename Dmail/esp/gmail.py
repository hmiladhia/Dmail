from Dmail import Email


class Gmail(Email):
    def __init__(self, sender_email, sender_password):
        super(Gmail, self).__init__(mail_server="smtp.gmail.com", mail_port=587,
                                    sender_email=sender_email, sender_password=sender_password)
