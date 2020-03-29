import smtplib
import ssl

from Dmail.mixin.email_base import EmailBase


class SmtpMixin(EmailBase):
    def __init__(self, mail_server, mail_port=None, sender_email=None, sender_credentials=None,
                 mail_use_tls=True, mail_use_ssl=False, *args, **kwargs):
        self._check_sanity(mail_server, mail_port, sender_email, sender_credentials, mail_use_tls, mail_use_ssl)

        # server info
        self.server = None
        self.mail_server = mail_server
        self.mail_port = mail_port
        self.mail_use_tls = mail_use_tls
        self.mail_use_ssl = mail_use_ssl

        # login info
        self.sender_email = sender_email
        self.sender_credentials = sender_credentials
        super(SmtpMixin, self).__init__(*args, sender_email=sender_email, **kwargs)

    def start(self, sender_email=None, sender_password=None):
        # server
        self.server = self.get_server(self.mail_server, self.mail_port, self.mail_use_tls, self.mail_use_ssl)

        # login
        sender_email = sender_email or self.sender_email
        sender_password = sender_password or self.sender_credentials
        if sender_password:
            self.server.login(sender_email, sender_password)
        super(SmtpMixin, self).start()

    def quit(self):
        self.server.quit()
        super(SmtpMixin, self).quit()

    def _send_email(self, email_recipient, email_body):
        self.server.sendmail(self.sender_email, email_recipient, email_body)

    @staticmethod
    def get_server(mail_server, mail_port, mail_use_tls, mail_use_ssl):
        if mail_use_ssl:
            context = ssl.create_default_context()
            server = smtplib.SMTP_SSL(mail_server, mail_port, context=context)
            server.ehlo()
        else:
            server = smtplib.SMTP(mail_server, mail_port)
            if mail_use_tls:
                server.ehlo()
                server.starttls()
                server.ehlo()
        return server

    @staticmethod
    def _check_sanity(mail_server, mail_port, sender_email, sender_credentials, mail_use_tls, mail_use_ssl):
        if mail_use_ssl and mail_use_tls:
            raise ValueError("Can't use TLS and SSL at the same time")
