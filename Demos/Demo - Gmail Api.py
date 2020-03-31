import os

from Dmail.api import GmailApi

recipient_email = "xxx@gmail.com"
sender_email = os.environ.get('email')

message = """
# Email Content
This is a **test**
"""

with GmailApi(sender_email, 'token.local.pickle', 'credentials.local.json') as email:
    email.send(message, recipient_email, '[Dmail]  Gmail Api - test')
    email.create_draft(message, recipient_email, '[Dmail]  Gmail Api - draft')
