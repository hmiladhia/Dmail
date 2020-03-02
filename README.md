# Dmail

This is a simple package that provides a simple way to send emails through code.

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

# list of email_id to send the mail
receiver_email = "xxx@gmail.com"
sender_email = os.environ.get('mail')
password = os.environ.get('pass')

message = """
    Email Content
"""

with Gmail(sender_email, password) as gmail:
    gmail.send_message(message, receiver_email, "Subject")

```

p.s. you are welcome to p

