import os
from Dmail import Gmail

# list of email_id to send the mail
receiver_email = "xxx@gmail.com"
sender_email = os.environ.get('mail')
password = os.environ.get('pass')

message = """
    Email Content
"""

with Gmail(sender_email, password) as gmail:
    gmail.send_message(message, receiver_email, "Subject")
