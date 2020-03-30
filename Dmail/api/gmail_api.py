from Dmail.mixin import MarkdownMixin, MimeMixin
from Dmail.api._gmail_api_base import GmailApiBase


class GmailApi(GmailApiBase, MarkdownMixin, MimeMixin):
    default_subtype = 'md'
    default_scope = 'compose'

    def __init__(self, sender_email, token_file='token.pickle', credentials_file=None, scopes='compose', md_extensions=None):
        super(GmailApi, self).__init__(sender_email=sender_email, token_file=token_file,
                                       credentials_file=credentials_file, scopes=scopes, md_extensions=md_extensions)

    def create_draft(self, email_text, to=None, subject=None, cc=None, bcc=None, subtype=None, attachments=None):
        subtype = subtype or self.default_subtype
        self._pre_send(email_text, to=to, subject=subject, cc=cc, bcc=bcc, subtype=subtype, attachments=attachments)
        email_body = self.get_message(email_text, to=to, subject=subject, cc=cc, bcc=bcc,
                                      subtype=subtype, attachments=attachments)
        self.createdraft(email_body)
        self._post_send(email_text, to=to, subject=subject, cc=cc, bcc=bcc, subtype=subtype, attachments=attachments)

    def createdraft(self, message):
        """Create and insert a draft email. Print the returned draft's message and id.

        Args:
          message: The body of the email message, including headers.

        Returns:
          Draft object, including draft id and message meta data.
        """
        body = {'message': self.get_request_body(message)}
        return self.service.users().drafts().create(userId=self.sender_email, body=body).execute()
