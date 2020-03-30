import base64
import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from Dmail.mixin import EmailBase


class GmailApiBase(EmailBase):
    default_scope = 'send'

    def __init__(self, sender_email, token_file, credentials_file=None, scopes='send', *args, **kwargs):
        super(GmailApiBase, self).__init__(*args, sender_email=sender_email, **kwargs)
        self.service = None
        self.creds = None

        self.set_creds(token_file, credentials_file, scopes)

    def set_creds(self, token_file, credentials_file=None, scopes=None):
        self.creds = None
        scopes = self.format_scopes(scopes or self.default_scope)
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid or set(self.creds.scopes) != set(scopes):
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if credentials_file is None:
                    raise ValueError('If no token has been created yet, you must specify the json credentials_file')
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, scopes)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_file, 'wb') as token:
                pickle.dump(self.creds, token)

    def start(self):
        self.service = build('gmail', 'v1', credentials=self.creds)
        super(GmailApiBase, self).start()

    def quit(self):
        self.service = None
        super(GmailApiBase, self).quit()

    def sendmail(self, recipients, message):
        body = self.get_request_body(message)
        message = (self.service.users().messages().send(userId=self.sender_email, body=body)
                   .execute())
        return message

    @staticmethod
    def get_request_body(message):
        return {'raw': base64.urlsafe_b64encode(message.encode()).decode()}

    @classmethod
    def format_scopes(cls, scopes):
        if isinstance(scopes, str):
            return [f'https://www.googleapis.com/auth/gmail.{scopes}']
        else:
            scopes_ = []
            for scope in scopes:
                scopes.extend(cls.format_scopes(scope))
            return scopes_
