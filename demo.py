import os
from Dmail import Gmail

# email info
receiver_email = "xxx@gmail.com"
sender_email = os.environ.get('mail')
password = os.environ.get('pass')

message = """
# Email Content
This is a **test**

![test image](tests/another_image.png)

this is some other text
"""

with Gmail(sender_email, password) as gmail:
    gmail.add_attachment(r"tests\test_image.jpg", "another_name.jpg")
    gmail.send_message(message, receiver_email, "Subject", subtype='md')
