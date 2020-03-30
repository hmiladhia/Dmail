import base64
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Dmail.mixin import EmailBase, MarkdownMixin, MimeMixin

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# SCOPES = ['https://www.googleapis.com/auth/gmail.send']
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


class GmailApiBase(EmailBase):
    def __init__(self, sender_email, token_file, credentials_file=None, *args, **kwargs):
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if credentials_file is None:
                    raise ValueError('If no token has been created yet, you must specify the json credentials_file')
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(self.creds, token)
        self.service = None
        super(GmailApiBase, self).__init__(*args, sender_email=sender_email, **kwargs)

    def start(self):
        self.service = build('gmail', 'v1', credentials=self.creds)
        super(GmailApiBase, self).start()

    def quit(self):
        self.service = None
        super(GmailApiBase, self).quit()

    def sendmail(self, recipients, message):
        try:
            body = {'raw': base64.urlsafe_b64encode(message.encode()).decode()}
            message = (self.service.users().messages().send(userId=self.sender_email, body=body)
                       .execute())
            # print('Message Id: %s' % message['id'])
            return message
        except Exception as error:
            print('An error occurred: %s' % error)


class GmailApi(GmailApiBase, MarkdownMixin, MimeMixin):
    default_subtype = 'md'

    def __init__(self, sender_email, token_file, credentials_file=None, md_extensions=None):
        super(GmailApi, self).__init__(sender_email=sender_email, token_file=token_file,
                                       credentials_file=credentials_file, md_extensions=md_extensions)

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
        try:
            body = {'message': {'raw': base64.urlsafe_b64encode(message.encode()).decode()}}
            return self.service.users().drafts().create(userId=self.sender_email, body=body).execute()
        except Exception as error:
            print('An error occurred: %s' % error)
            return None
