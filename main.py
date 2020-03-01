import os
from Dmail import Gmail

# list of email_id to send the mail
receiver = "xxx@gmail.com"
email_id = os.environ.get('mail')
password = os.environ.get('pass')

message = """
    Contenu du message
"""

with Gmail(email_id, password) as gmail:
    gmail.send_message(message, receiver, "Object")
