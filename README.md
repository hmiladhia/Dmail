# Dmail

This is a simple package that provides a simple way to send emails through code.

It has the possibility to send markdown content ( that is converted to html )

![Steins;Gate](https://media.giphy.com/media/jGJWV3AnjiC4M/giphy.gif)

## Installation

A simple pip install will do :

```bash
python -m pip install Dmail
```

## Demo

```python
import os
from Dmail import Gmail

# email info
receiver_email = "xxx@gmail.com"
sender_email = os.environ.get('mail')
password = os.environ.get('pass')

message = """
    Email Content
"""

with Gmail(sender_email, password) as gmail:
    gmail.send_message(message, receiver_email, "Subject")

# Send Markdown e-mails :
message = """
# Email Content
This is a **test**

![test image](tests/another_image.png)

this is some other text
"""

with Gmail(sender_email, password) as gmail:
    gmail.add_attachment(r"tests\test_image.jpg", "another_name.jpg")
    gmail.send_message(message, receiver_email, "Subject", subtype='md')


```
