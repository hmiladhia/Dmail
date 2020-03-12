from Dmail import Email


class Hotmail(Email):
    def __init__(self, sender_email, sender_password):
        super(Hotmail, self).__init__(mail_server="smtp.live.com", mail_port=587,
                                      sender_email=sender_email, sender_password=sender_password)
